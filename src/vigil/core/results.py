"""Test result data structures."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TestResult:
    """Result from running an agent."""

    output: str
    cost: float | None = None
    tokens_input: int | None = None
    tokens_output: int | None = None
    latency: float | None = None
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def tokens_total(self) -> int | None:
        if self.tokens_input is not None and self.tokens_output is not None:
            return self.tokens_input + self.tokens_output
        return None

    def __str__(self) -> str:
        return self.output


class Timer:
    """Context manager to measure elapsed time."""

    def __init__(self) -> None:
        self.start: float = 0
        self.end: float = 0
        self.elapsed: float = 0

    def __enter__(self) -> Timer:
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args: Any) -> None:
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
