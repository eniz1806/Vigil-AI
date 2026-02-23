"""Vigil plugin system — register custom assertions, agents, and reporters."""

from vigil.plugins.registry import (
    registry,
    register_assertion,
    register_agent,
    register_reporter,
    get_assertion,
    get_agent,
    get_reporter,
    load_plugins,
)

__all__ = [
    "registry",
    "register_assertion",
    "register_agent",
    "register_reporter",
    "get_assertion",
    "get_agent",
    "get_reporter",
    "load_plugins",
]
