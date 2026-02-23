"""Vigil — The testing framework for AI agents."""

__version__ = "0.1.0"

from vigil.core.decorators import test
from vigil.core.results import TestResult
from vigil.agents import FunctionAgent, HTTPAgent, CLIAgent
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

__all__ = [
    "test",
    "TestResult",
    "FunctionAgent",
    "HTTPAgent",
    "CLIAgent",
    "assert_contains",
    "assert_not_contains",
    "assert_json_valid",
    "assert_matches_regex",
    "assert_cost_under",
    "assert_tokens_under",
    "assert_latency_under",
    "assert_semantic_match",
    "assert_no_hallucination",
]
