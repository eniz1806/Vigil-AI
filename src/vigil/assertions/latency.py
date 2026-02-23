"""Latency assertions."""

from __future__ import annotations

from vigil.core.results import TestResult


def assert_latency_under(result: TestResult, max_seconds: float) -> None:
    """Assert that the response latency is under the threshold."""
    if result.latency is None:
        raise AssertionError(
            "Cannot check latency: result has no latency data. "
            "Ensure your agent tracks latency in TestResult.latency"
        )
    if result.latency > max_seconds:
        raise AssertionError(
            f"Latency {result.latency:.3f}s exceeds threshold {max_seconds:.3f}s"
        )
