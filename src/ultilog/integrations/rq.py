"""RQ (Redis Queue) integration helpers for ``ultilog``.

Purpose
-------
Bind logging context around RQ worker job execution.

Design
------
The helper patches the RQ worker's ``perform_job`` method to wrap each job
in a logging context with the job ID and function name.
"""

from __future__ import annotations

from typing import Any

from ultilog.context.managers import logging_context
from ultilog.utils.import_tools import require_module


def install_rq_logging(worker: Any) -> Any:
    """Install ultilog context binding on an RQ worker.

    Wraps the worker's ``perform_job`` to bind ``rq_job_id`` and
    ``rq_func_name`` into logging context for each job execution.

    Args:
        worker: An ``rq.Worker`` instance.

    Returns:
        The same worker for fluent usage.

    Raises:
        UltilogOptionalDependencyError: If rq is not installed.

    Examples:
        >>> install_rq_logging(worker)  # doctest: +SKIP
    """
    require_module("rq", extra="rq")

    original_perform = worker.perform_job

    def _wrapped_perform(job: Any, queue: Any) -> Any:
        with logging_context(
            rq_job_id=job.id,
            rq_func_name=job.func_name,
        ):
            return original_perform(job, queue)

    worker.perform_job = _wrapped_perform
    return worker


__all__ = ["install_rq_logging"]
