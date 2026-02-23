"""Content-based assertions."""

from __future__ import annotations

import json
import re

from vigil.core.results import TestResult


def _get_output(result: TestResult | str) -> str:
    if isinstance(result, TestResult):
        return result.output
    return result


def assert_contains(result: TestResult | str, expected: str, case_sensitive: bool = True) -> None:
    """Assert that the output contains the expected text."""
    output = _get_output(result)
    if case_sensitive:
        if expected not in output:
            raise AssertionError(
                f"Expected output to contain '{expected}'\n"
                f"Got: '{output[:200]}{'...' if len(output) > 200 else ''}'"
            )
    else:
        if expected.lower() not in output.lower():
            raise AssertionError(
                f"Expected output to contain '{expected}' (case-insensitive)\n"
                f"Got: '{output[:200]}{'...' if len(output) > 200 else ''}'"
            )


def assert_not_contains(
    result: TestResult | str, unexpected: str, case_sensitive: bool = True
) -> None:
    """Assert that the output does NOT contain the text."""
    output = _get_output(result)
    if case_sensitive:
        if unexpected in output:
            raise AssertionError(f"Expected output to NOT contain '{unexpected}'\nBut it was found.")
    else:
        if unexpected.lower() in output.lower():
            raise AssertionError(
                f"Expected output to NOT contain '{unexpected}' (case-insensitive)\n"
                f"But it was found."
            )


def assert_json_valid(result: TestResult | str) -> dict:
    """Assert that the output is valid JSON. Returns the parsed dict."""
    output = _get_output(result)
    try:
        return json.loads(output)
    except (json.JSONDecodeError, TypeError) as e:
        raise AssertionError(
            f"Expected valid JSON output\n"
            f"Parse error: {e}\n"
            f"Got: '{output[:200]}{'...' if len(output) > 200 else ''}'"
        ) from e


def assert_matches_regex(result: TestResult | str, pattern: str) -> re.Match:
    """Assert that the output matches the regex pattern. Returns the match object."""
    output = _get_output(result)
    match = re.search(pattern, output)
    if not match:
        raise AssertionError(
            f"Expected output to match pattern '{pattern}'\n"
            f"Got: '{output[:200]}{'...' if len(output) > 200 else ''}'"
        )
    return match
