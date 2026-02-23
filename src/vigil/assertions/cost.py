"""Cost and token usage assertions."""

from __future__ import annotations

from vigil.core.results import TestResult


def assert_cost_under(result: TestResult, max_dollars: float) -> None:
    """Assert that the API cost is under the threshold."""
    if result.cost is None:
        raise AssertionError(
            "Cannot check cost: result has no cost data. "
            "Ensure your agent tracks cost in TestResult.cost"
        )
    if result.cost > max_dollars:
        raise AssertionError(
            f"Cost ${result.cost:.4f} exceeds threshold ${max_dollars:.4f}\n"
            f"Model: {result.model or 'unknown'}"
        )


def assert_tokens_under(result: TestResult, max_tokens: int) -> None:
    """Assert that total token usage is under the threshold."""
    total = result.tokens_total
    if total is None:
        raise AssertionError(
            "Cannot check tokens: result has no token data. "
            "Ensure your agent tracks tokens in TestResult"
        )
    if total > max_tokens:
        raise AssertionError(
            f"Token usage {total} exceeds threshold {max_tokens}\n"
            f"Input: {result.tokens_input}, Output: {result.tokens_output}"
        )
