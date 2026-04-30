"""Queue logging helpers for ``ultilog``.

Purpose
-------
Provide queue-based handler factories for applications that want non-blocking
or centralized logging pipelines.

Design
------
This module stays close to the standard library's ``logging.handlers`` queue
interfaces so future workers, listeners, and OpenTelemetry exporters can reuse
it without special package-specific abstractions.

Examples
--------
.. code-block:: python

    from queue import SimpleQueue
    from ultilog.handlers.queue import create_queue_handler

    handler = create_queue_handler(SimpleQueue())
"""

from __future__ import annotations

import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue, SimpleQueue
from typing import Any

QueueLike = Queue[Any] | SimpleQueue[Any]


def create_queue_handler(queue: QueueLike, *, level: int = logging.NOTSET) -> QueueHandler:
    """Create a queue handler.

    Args:
        queue: Queue-like object that receives ``LogRecord`` instances.
        level: Handler-level threshold.

    Returns:
        Configured ``QueueHandler``.

    Raises:
        None.

    Examples:
        >>> from queue import SimpleQueue
        >>> create_queue_handler(SimpleQueue()).level == logging.NOTSET
        True
    """
    handler = QueueHandler(queue)
    handler.setLevel(level)
    return handler


def create_queue_listener(queue: QueueLike, *handlers: logging.Handler) -> QueueListener:
    """Create a queue listener.

    Args:
        queue: Queue-like object used by matching queue handlers.
        *handlers: Handlers that consume records from the listener.

    Returns:
        Configured ``QueueListener``.

    Raises:
        None.

    Examples:
        >>> from queue import SimpleQueue
        >>> listener = create_queue_listener(SimpleQueue())
        >>> listener.handlers
        ()
    """
    return QueueListener(queue, *handlers)


__all__ = ["QueueLike", "create_queue_handler", "create_queue_listener"]
