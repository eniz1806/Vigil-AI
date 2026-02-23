"""Tests for Vigil agent runners."""

import pytest

from vigil.core.results import TestResult
from vigil.agents.function import FunctionAgent


class TestFunctionAgent:
    def test_string_return(self):
        def echo(msg: str) -> str:
            return f"echo: {msg}"

        agent = FunctionAgent(echo)
        result = agent.run("hello")
        assert result.output == "echo: hello"
        assert result.latency is not None
        assert result.latency >= 0

    def test_dict_return(self):
        def smart_agent(msg: str) -> dict:
            return {
                "output": f"response to {msg}",
                "cost": 0.001,
                "tokens_input": 10,
                "tokens_output": 20,
                "model": "test-model",
            }

        agent = FunctionAgent(smart_agent)
        result = agent.run("test")
        assert result.output == "response to test"
        assert result.cost == 0.001
        assert result.tokens_input == 10
        assert result.tokens_output == 20
        assert result.tokens_total == 30
        assert result.model == "test-model"

    def test_result_return(self):
        def agent_fn(msg: str) -> TestResult:
            return TestResult(output="direct result", cost=0.05)

        agent = FunctionAgent(agent_fn)
        result = agent.run("test")
        assert result.output == "direct result"
        assert result.cost == 0.05
        assert result.latency is not None

    def test_default_kwargs(self):
        def agent_fn(msg: str, temperature: float = 0.7) -> str:
            return f"temp={temperature}"

        agent = FunctionAgent(agent_fn, temperature=0.0)
        result = agent.run("test")
        assert result.output == "temp=0.0"

    def test_override_kwargs(self):
        def agent_fn(msg: str, temperature: float = 0.7) -> str:
            return f"temp={temperature}"

        agent = FunctionAgent(agent_fn, temperature=0.0)
        result = agent.run("test", temperature=1.0)
        assert result.output == "temp=1.0"

    def test_exception_propagates(self):
        def bad_agent(msg: str) -> str:
            raise ValueError("agent crashed")

        agent = FunctionAgent(bad_agent)
        with pytest.raises(ValueError, match="agent crashed"):
            agent.run("test")
