"""Demo application services."""

from __future__ import annotations

from ultilog import get_logger, logging_context

log = get_logger(__name__)


def process_order(order_id: str, *, user_id: str) -> dict[str, str]:
    """Process a fake order."""
    with logging_context(order_id=order_id, user_id=user_id):
        log.info("order.started")
        log.info("order.validated")
        log.info("order.completed")
    return {"order_id": order_id, "status": "completed"}
