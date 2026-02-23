"""Function agent — wraps a Python callable as a testable agent."""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable

from vigil.core.results import TestResult, Timer


class FunctionAgent:
    """Wraps any Python function (sync or async) as an agent under test.

    The function can return:
        - A string (output only)
        - A dict with keys: output, cost, tokens_input, tokens_output, model, metadata
        - A TestResult directly

    Example:
        def my_chatbot(message: str) -> str:
            return openai.chat(message)

        agent = FunctionAgent(my_chatbot)
        result = agent.run("Hello!")
    """

    def __init__(self, func: Callable, **default_kwargs: Any) -> None:
        self.func = func
        self.default_kwargs = default_kwargs

    def run(self, input: str, **kwargs: Any) -> TestResult:
        merged = {**self.default_kwargs, **kwargs}
        timer = Timer()

        with timer:
            if inspect.iscoroutinefunction(self.func):
                raw = asyncio.get_event_loop().run_until_complete(self.func(input, **merged))
            else:
                raw = self.func(input, **merged)

        return self._to_result(raw, timer.elapsed)

    def _to_result(self, raw: Any, elapsed: float) -> TestResult:
        if isinstance(raw, TestResult):
            if raw.latency is None:
                raw.latency = elapsed
            return raw

        if isinstance(raw, dict):
            return TestResult(
                output=str(raw.get("output", "")),
                cost=raw.get("cost"),
                tokens_input=raw.get("tokens_input"),
                tokens_output=raw.get("tokens_output"),
                model=raw.get("model"),
                latency=raw.get("latency", elapsed),
                metadata=raw.get("metadata", {}),
            )

        return TestResult(output=str(raw), latency=elapsed)
