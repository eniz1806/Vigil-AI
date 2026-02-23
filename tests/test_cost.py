"""Tests for cost tracking."""

import pytest

from vigil.cost import calculate_cost, enrich_result, list_models, get_pricing
from vigil.core.results import TestResult


class TestCalculateCost:
    def test_known_model(self):
        cost = calculate_cost("gpt-4o-mini", tokens_input=1000, tokens_output=500)
        assert cost is not None
        assert cost > 0
        # gpt-4o-mini: $0.15/M input, $0.60/M output
        expected = (1000 * 0.15 + 500 * 0.60) / 1_000_000
        assert abs(cost - expected) < 0.0001

    def test_unknown_model(self):
        cost = calculate_cost("some-unknown-model", tokens_input=1000, tokens_output=500)
        assert cost is None

    def test_alias(self):
        cost = calculate_cost("haiku", tokens_input=1000, tokens_output=500)
        assert cost is not None

    def test_partial_match(self):
        cost = calculate_cost("gpt-4o", tokens_input=1000, tokens_output=500)
        assert cost is not None


class TestEnrichResult:
    def test_enriches_with_cost(self):
        result = TestResult(
            output="test",
            model="gpt-4o-mini",
            tokens_input=100,
            tokens_output=50,
        )
        enrich_result(result)
        assert result.cost is not None
        assert result.cost > 0

    def test_skips_if_cost_exists(self):
        result = TestResult(output="test", cost=0.99, model="gpt-4o-mini",
                            tokens_input=100, tokens_output=50)
        enrich_result(result)
        assert result.cost == 0.99

    def test_skips_if_no_model(self):
        result = TestResult(output="test", tokens_input=100, tokens_output=50)
        enrich_result(result)
        assert result.cost is None


class TestHelpers:
    def test_list_models(self):
        models = list_models()
        assert len(models) > 5
        assert "gpt-4o" in models

    def test_get_pricing(self):
        pricing = get_pricing("gpt-4o-mini")
        assert pricing is not None
        assert pricing == (0.15, 0.60)

    def test_get_pricing_unknown(self):
        assert get_pricing("nonexistent") is None
