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

        # Async functions work too:
        async def my_async_agent(message: str) -> str:
            return await some_api.call(message)

        agent = FunctionAgent(my_async_agent)
        result = await agent.arun("Hello!")
    """

    def __init__(self, func: Callable, **default_kwargs: Any) -> None:
        self.func = func
        self.default_kwargs = default_kwargs
        self._is_async = inspect.iscoroutinefunction(func)

    def run(self, input: str, **kwargs: Any) -> TestResult:
        """Run the agent synchronously. Async functions are handled automatically."""
        merged = {**self.default_kwargs, **kwargs}
        timer = Timer()

        with timer:
            if self._is_async:
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop and loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as pool:
                        raw = pool.submit(
                            asyncio.run, self.func(input, **merged)
                        ).result()
                else:
                    raw = asyncio.run(self.func(input, **merged))
            else:
                raw = self.func(input, **merged)

        return self._to_result(raw, timer.elapsed)

    async def arun(self, input: str, **kwargs: Any) -> TestResult:
        """Run the agent asynchronously."""
        merged = {**self.default_kwargs, **kwargs}
        timer = Timer()

        with timer:
            if self._is_async:
                raw = await self.func(input, **merged)
            else:
                loop = asyncio.get_running_loop()
                raw = await loop.run_in_executor(None, self.func, input, **merged) if not merged else await loop.run_in_executor(None, lambda: self.func(input, **merged))

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
