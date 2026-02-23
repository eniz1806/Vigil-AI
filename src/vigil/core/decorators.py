"""Test decorators."""

from __future__ import annotations

import functools
from typing import Any, Callable


def test(
    name: str | None = None,
    tags: list[str] | None = None,
    steps: bool = False,
) -> Callable:
    """Mark a function as a Vigil AI test.

    Args:
        name: Optional display name for the test.
        tags: Optional tags for filtering tests.
        steps: If True, the test is a multi-step conversation test.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        wrapper._vigil_test = True  # type: ignore[attr-defined]
        wrapper._vigil_name = name or func.__name__  # type: ignore[attr-defined]
        wrapper._vigil_tags = tags or []  # type: ignore[attr-defined]
        wrapper._vigil_steps = steps  # type: ignore[attr-defined]
        return wrapper

    return decorator
