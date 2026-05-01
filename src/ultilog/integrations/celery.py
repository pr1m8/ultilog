"""Celery integration helpers for ``ultilog``.

Purpose
-------
Bind logging context around Celery task execution so log records carry task
metadata automatically.

Design
------
The helper connects to Celery signals lazily.  It does not import Celery at
module level so applications that do not use Celery pay no cost.
"""

from __future__ import annotations

from typing import Any

from ultilog.context.vars import bind_context, clear_context
from ultilog.utils.import_tools import require_module


def install_celery_logging(app: Any) -> Any:
    """Install ultilog context binding on a Celery application.

    Connects ``task_prerun`` and ``task_postrun`` signals so every task
    execution gets logging context with the task name and task ID.

    Args:
        app: Celery application instance.

    Returns:
        The same app object for fluent usage.

    Raises:
        UltilogOptionalDependencyError: If celery is not installed.

    Examples:
        >>> install_celery_logging(app)  # doctest: +SKIP
    """
    require_module("celery", extra="celery")

    from celery.signals import task_postrun, task_prerun  # type: ignore[import-not-found]

    @task_prerun.connect  # type: ignore[untyped-decorator]
    def _on_task_prerun(
        sender: Any = None,
        task_id: str | None = None,
        task: Any = None,
        **kwargs: Any,
    ) -> None:
        bind_context(
            celery_task_id=task_id or "",
            celery_task_name=getattr(task, "name", str(sender)),
        )

    @task_postrun.connect  # type: ignore[untyped-decorator]
    def _on_task_postrun(**kwargs: Any) -> None:
        clear_context()

    return app


__all__ = ["install_celery_logging"]
