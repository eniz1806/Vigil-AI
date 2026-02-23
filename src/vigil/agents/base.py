"""Base agent protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from vigil.core.results import TestResult


@runtime_checkable
class AgentUnderTest(Protocol):
    """Protocol for any agent that can be tested with Vigil."""

    def run(self, input: str, **kwargs: Any) -> TestResult:
        """Run the agent with the given input and return a TestResult."""
        ...
