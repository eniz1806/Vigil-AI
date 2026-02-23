"""HTTP agent — test agents exposed as HTTP endpoints."""

from __future__ import annotations

from typing import Any

from vigil.core.results import TestResult, Timer


class HTTPAgent:
    """Wraps an HTTP endpoint as an agent under test.

    Sends POST requests with {"input": "..."} and expects
    a JSON response with at least an "output" field.

    Example:
        agent = HTTPAgent("http://localhost:8000/chat")
        result = agent.run("Hello!")

        # Async:
        result = await agent.arun("Hello!")
    """

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        input_key: str = "input",
        output_key: str = "output",
        timeout: float = 30.0,
    ) -> None:
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
        self.input_key = input_key
        self.output_key = output_key
        self.timeout = timeout

    def run(self, input: str, **kwargs: Any) -> TestResult:
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "httpx is required for HTTPAgent. Install with: pip install vigil-ai[http]"
            )

        payload = {self.input_key: input, **kwargs}
        timer = Timer()

        with timer:
            response = httpx.post(
                self.url,
                json=payload,
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

        data = response.json()

        return TestResult(
            output=str(data.get(self.output_key, "")),
            cost=data.get("cost"),
            tokens_input=data.get("tokens_input"),
            tokens_output=data.get("tokens_output"),
            model=data.get("model"),
            latency=timer.elapsed,
            metadata=data.get("metadata", {}),
        )

    async def arun(self, input: str, **kwargs: Any) -> TestResult:
        """Run the agent asynchronously using httpx.AsyncClient."""
        try:
            import httpx
        except ImportError:
            raise ImportError(
                "httpx is required for HTTPAgent. Install with: pip install vigil-ai[http]"
            )

        payload = {self.input_key: input, **kwargs}
        timer = Timer()

        with timer:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    json=payload,
                    headers=self.headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()

        data = response.json()

        return TestResult(
            output=str(data.get(self.output_key, "")),
            cost=data.get("cost"),
            tokens_input=data.get("tokens_input"),
            tokens_output=data.get("tokens_output"),
            model=data.get("model"),
            latency=timer.elapsed,
            metadata=data.get("metadata", {}),
        )
