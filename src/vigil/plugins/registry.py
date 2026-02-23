"""Plugin registry — central hub for all Vigil extensions.

Plugins can be registered in three ways:

1. Decorator:
    @register_assertion("assert_tone")
    def assert_tone(result, expected_tone, **kwargs):
        ...

2. Entry points (in plugin's pyproject.toml):
    [project.entry-points."vigil.assertions"]
    assert_tone = "my_plugin:assert_tone"

3. Programmatic:
    registry.assertions["assert_tone"] = assert_tone
"""

from __future__ import annotations

import importlib.metadata
import logging
from typing import Any, Callable, Protocol, runtime_checkable

logger = logging.getLogger("vigil.plugins")


@runtime_checkable
class ReporterProtocol(Protocol):
    def add_result(self, name: str, passed: bool, **kwargs: Any) -> None: ...
    def render(self) -> Any: ...


class PluginRegistry:
    """Central registry for Vigil plugins."""

    def __init__(self) -> None:
        self.assertions: dict[str, Callable] = {}
        self.agents: dict[str, type] = {}
        self.reporters: dict[str, type] = {}
        self._loaded = False

    def register_assertion(self, name: str, func: Callable) -> None:
        self.assertions[name] = func
        logger.debug(f"Registered assertion: {name}")

    def register_agent(self, name: str, cls: type) -> None:
        self.agents[name] = cls
        logger.debug(f"Registered agent: {name}")

    def register_reporter(self, name: str, cls: type) -> None:
        self.reporters[name] = cls
        logger.debug(f"Registered reporter: {name}")

    def load_entry_points(self) -> None:
        """Discover and load plugins from entry points."""
        if self._loaded:
            return
        self._loaded = True

        for group, target in [
            ("vigil.assertions", self.assertions),
            ("vigil.agents", self.agents),
            ("vigil.reporters", self.reporters),
        ]:
            try:
                eps = importlib.metadata.entry_points(group=group)
            except TypeError:
                # Python 3.9 compat
                eps = importlib.metadata.entry_points().get(group, [])

            for ep in eps:
                try:
                    obj = ep.load()
                    target[ep.name] = obj
                    logger.debug(f"Loaded plugin {group}:{ep.name}")
                except Exception as e:
                    logger.warning(f"Failed to load plugin {group}:{ep.name}: {e}")

    def list_plugins(self) -> dict[str, list[str]]:
        """List all registered plugins."""
        self.load_entry_points()
        return {
            "assertions": list(self.assertions.keys()),
            "agents": list(self.agents.keys()),
            "reporters": list(self.reporters.keys()),
        }


# Global registry instance
registry = PluginRegistry()


def register_assertion(name: str) -> Callable:
    """Decorator to register a custom assertion.

    Example:
        @register_assertion("assert_polite")
        def assert_polite(result, **kwargs):
            output = result.output if hasattr(result, 'output') else str(result)
            if any(word in output.lower() for word in ["please", "thank", "sorry"]):
                return
            raise AssertionError("Output is not polite")
    """
    def decorator(func: Callable) -> Callable:
        registry.register_assertion(name, func)
        return func
    return decorator


def register_agent(name: str) -> Callable:
    """Decorator to register a custom agent type.

    Example:
        @register_agent("websocket")
        class WebSocketAgent:
            def run(self, input: str, **kwargs) -> TestResult:
                ...
    """
    def decorator(cls: type) -> type:
        registry.register_agent(name, cls)
        return cls
    return decorator


def register_reporter(name: str) -> Callable:
    """Decorator to register a custom reporter.

    Example:
        @register_reporter("slack")
        class SlackReporter:
            def add_result(self, name, passed, **kwargs): ...
            def render(self): ...
    """
    def decorator(cls: type) -> type:
        registry.register_reporter(name, cls)
        return cls
    return decorator


def get_assertion(name: str) -> Callable:
    """Get a registered assertion by name."""
    registry.load_entry_points()
    if name not in registry.assertions:
        available = ", ".join(registry.assertions.keys()) or "none"
        raise KeyError(f"Unknown assertion '{name}'. Available: {available}")
    return registry.assertions[name]


def get_agent(name: str) -> type:
    """Get a registered agent type by name."""
    registry.load_entry_points()
    if name not in registry.agents:
        available = ", ".join(registry.agents.keys()) or "none"
        raise KeyError(f"Unknown agent '{name}'. Available: {available}")
    return registry.agents[name]


def get_reporter(name: str) -> type:
    """Get a registered reporter by name."""
    registry.load_entry_points()
    if name not in registry.reporters:
        available = ", ".join(registry.reporters.keys()) or "none"
        raise KeyError(f"Unknown reporter '{name}'. Available: {available}")
    return registry.reporters[name]


def load_plugins() -> None:
    """Explicitly load all plugins from entry points."""
    registry.load_entry_points()
