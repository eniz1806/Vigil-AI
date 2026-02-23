"""Tests for Vigil assertions."""

import pytest

from vigil.core.results import TestResult
from vigil.assertions.content import (
    assert_contains,
    assert_not_contains,
    assert_json_valid,
    assert_matches_regex,
)
from vigil.assertions.cost import assert_cost_under, assert_tokens_under
from vigil.assertions.latency import assert_latency_under
from vigil.assertions.semantic import assert_semantic_match
from vigil.assertions.quality import assert_no_hallucination


# --- Content assertions ---


class TestAssertContains:
    def test_pass_with_string(self):
        assert_contains("hello world", "hello")

    def test_pass_with_result(self):
        result = TestResult(output="hello world")
        assert_contains(result, "hello")

    def test_fail(self):
        with pytest.raises(AssertionError, match="Expected output to contain"):
            assert_contains("hello world", "goodbye")

    def test_case_insensitive(self):
        assert_contains("Hello World", "hello", case_sensitive=False)

    def test_case_sensitive_fail(self):
        with pytest.raises(AssertionError):
            assert_contains("Hello World", "hello", case_sensitive=True)


class TestAssertNotContains:
    def test_pass(self):
        assert_not_contains("hello world", "goodbye")

    def test_fail(self):
        with pytest.raises(AssertionError, match="NOT contain"):
            assert_not_contains("hello world", "hello")


class TestAssertJsonValid:
    def test_valid_json(self):
        data = assert_json_valid('{"key": "value"}')
        assert data == {"key": "value"}

    def test_invalid_json(self):
        with pytest.raises(AssertionError, match="valid JSON"):
            assert_json_valid("not json")

    def test_with_result(self):
        result = TestResult(output='[1, 2, 3]')
        data = assert_json_valid(result)
        assert data == [1, 2, 3]


class TestAssertMatchesRegex:
    def test_pass(self):
        match = assert_matches_regex("error code: 404", r"code: (\d+)")
        assert match.group(1) == "404"

    def test_fail(self):
        with pytest.raises(AssertionError, match="match pattern"):
            assert_matches_regex("hello world", r"\d+")


# --- Cost assertions ---


class TestAssertCostUnder:
    def test_pass(self):
        result = TestResult(output="ok", cost=0.001)
        assert_cost_under(result, 0.01)

    def test_fail(self):
        result = TestResult(output="ok", cost=0.05)
        with pytest.raises(AssertionError, match="exceeds threshold"):
            assert_cost_under(result, 0.01)

    def test_no_cost_data(self):
        result = TestResult(output="ok")
        with pytest.raises(AssertionError, match="no cost data"):
            assert_cost_under(result, 0.01)


class TestAssertTokensUnder:
    def test_pass(self):
        result = TestResult(output="ok", tokens_input=50, tokens_output=50)
        assert_tokens_under(result, 200)

    def test_fail(self):
        result = TestResult(output="ok", tokens_input=500, tokens_output=500)
        with pytest.raises(AssertionError, match="exceeds threshold"):
            assert_tokens_under(result, 200)


# --- Latency assertions ---


class TestAssertLatencyUnder:
    def test_pass(self):
        result = TestResult(output="ok", latency=0.5)
        assert_latency_under(result, 1.0)

    def test_fail(self):
        result = TestResult(output="ok", latency=5.0)
        with pytest.raises(AssertionError, match="exceeds threshold"):
            assert_latency_under(result, 1.0)


# --- Semantic assertions ---


class TestAssertSemanticMatch:
    def test_identical(self):
        assert_semantic_match("hello world", "hello world", threshold=0.9)

    def test_similar(self):
        assert_semantic_match(
            "Python is a programming language",
            "Python is a popular programming language for developers",
            threshold=0.3,
        )

    def test_dissimilar(self):
        with pytest.raises(AssertionError, match="below threshold"):
            assert_semantic_match("cats are cute", "quantum physics is complex", threshold=0.5)

    def test_with_result(self):
        result = TestResult(output="Python is great for data science")
        assert_semantic_match(result, "Python is used in data science", threshold=0.3)


# --- Quality assertions ---


class TestAssertNoHallucination:
    def test_grounded(self):
        context = "Python was created by Guido van Rossum in 1991. It is a high-level programming language."
        output = "Python is a high-level programming language created by Guido van Rossum."
        assert_no_hallucination(output, context)

    def test_hallucination(self):
        context = "Python was created by Guido van Rossum in 1991."
        output = "Python was created by Elon Musk in 2020 for space exploration."
        with pytest.raises(AssertionError, match="hallucination"):
            assert_no_hallucination(output, context, threshold=0.5)

    def test_with_result(self):
        context = "The sky is blue. Water is wet."
        result = TestResult(output="The sky is blue and water is wet.")
        assert_no_hallucination(result, context)
