"""CLI agent — test agents exposed as command-line tools."""

from __future__ import annotations

import asyncio
import subprocess
from typing import Any

from vigil.core.results import TestResult, Timer


class CLIAgent:
    """Wraps a CLI command as an agent under test.

    Runs the command with the input as an argument and captures stdout.

    Example:
        agent = CLIAgent("python my_agent.py")
        result = agent.run("Hello!")

        # Or with stdin mode:
        agent = CLIAgent("python my_agent.py", input_mode="stdin")
        result = agent.run("Hello!")
    """

    def __init__(
        self,
        command: str,
        input_mode: str = "arg",
        timeout: float = 60.0,
        env: dict[str, str] | None = None,
    ) -> None:
        self.command = command
        self.input_mode = input_mode
        self.timeout = timeout
        self.env = env

    def run(self, input: str, **kwargs: Any) -> TestResult:
        timer = Timer()

        if self.input_mode == "stdin":
            cmd = self.command
            stdin_data = input
        else:
            cmd = f"{self.command} {repr(input)}"
            stdin_data = None

        with timer:
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                input=stdin_data,
                env=self.env,
            )

        if proc.returncode != 0:
            raise RuntimeError(
                f"Agent command failed with exit code {proc.returncode}\n"
                f"stderr: {proc.stderr[:500]}"
            )

        return TestResult(output=proc.stdout.strip(), latency=timer.elapsed)

    async def arun(self, input: str, **kwargs: Any) -> TestResult:
        """Run the agent asynchronously using asyncio subprocess."""
        timer = Timer()

        if self.input_mode == "stdin":
            cmd = self.command
            stdin_data = input.encode()
        else:
            cmd = f"{self.command} {repr(input)}"
            stdin_data = None

        with timer:
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if stdin_data else None,
                env=self.env,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=stdin_data),
                timeout=self.timeout,
            )

        if proc.returncode != 0:
            raise RuntimeError(
                f"Agent command failed with exit code {proc.returncode}\n"
                f"stderr: {stderr.decode()[:500]}"
            )

        return TestResult(output=stdout.decode().strip(), latency=timer.elapsed)
