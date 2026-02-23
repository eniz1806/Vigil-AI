"""Tests for async agent support."""

import pytest

from vigil.agents.function import FunctionAgent
from vigil.core.results import TestResult


class TestAsyncFunctionAgent:
    def test_async_string_return(self):
        async def async_echo(msg: str) -> str:
            return f"async: {msg}"

        agent = FunctionAgent(async_echo)
        result = agent.run("hello")
        assert result.output == "async: hello"
        assert result.latency is not None

    def test_async_dict_return(self):
        async def async_agent(msg: str) -> dict:
            return {"output": f"response to {msg}", "cost": 0.002, "model": "test"}

        agent = FunctionAgent(async_agent)
        result = agent.run("test")
        assert result.output == "response to test"
        assert result.cost == 0.002

    def test_async_result_return(self):
        async def async_agent(msg: str) -> TestResult:
            return TestResult(output="direct", cost=0.01)

        agent = FunctionAgent(async_agent)
        result = agent.run("test")
        assert result.output == "direct"
        assert result.cost == 0.01

    def test_is_async_flag(self):
        async def async_fn(msg: str) -> str:
            return msg

        def sync_fn(msg: str) -> str:
            return msg

        assert FunctionAgent(async_fn)._is_async is True
        assert FunctionAgent(sync_fn)._is_async is False
