"""Tests for request context helpers."""

from __future__ import annotations

from ultilog.context.request import request_context_values


def test_request_context_includes_method_and_path() -> None:
    data = request_context_values(method="GET", path="/health")
    assert data["http.method"] == "GET"
    assert data["http.path"] == "/health"


def test_request_context_generates_request_id() -> None:
    data = request_context_values()
    assert "request_id" in data
    assert len(data["request_id"]) > 0


def test_request_context_uses_provided_request_id() -> None:
    data = request_context_values(request_id="custom-123")
    assert data["request_id"] == "custom-123"


def test_request_context_includes_optional_fields() -> None:
    data = request_context_values(
        client="10.0.0.1",
        user_agent="TestAgent/1.0",
    )
    assert data["client"] == "10.0.0.1"
    assert data["user_agent"] == "TestAgent/1.0"


def test_request_context_passes_extra_kwargs() -> None:
    data = request_context_values(custom_field="value")
    assert data["custom_field"] == "value"
