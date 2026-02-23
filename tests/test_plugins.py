"""Tests for the plugin system."""

import pytest

from vigil.plugins.registry import (
    PluginRegistry,
    register_assertion,
    register_agent,
    register_reporter,
)
from vigil.core.results import TestResult


class TestPluginRegistry:
    def test_register_assertion(self):
        reg = PluginRegistry()
        reg.register_assertion("test_assert", lambda r: None)
        assert "test_assert" in reg.assertions

    def test_register_agent(self):
        reg = PluginRegistry()

        class MyAgent:
            pass

        reg.register_agent("my_agent", MyAgent)
        assert "my_agent" in reg.agents

    def test_register_reporter(self):
        reg = PluginRegistry()

        class MyReporter:
            pass

        reg.register_reporter("my_reporter", MyReporter)
        assert "my_reporter" in reg.reporters

    def test_list_plugins(self):
        reg = PluginRegistry()
        reg.register_assertion("a1", lambda: None)
        reg.register_agent("ag1", type)
        plugins = reg.list_plugins()
        assert "a1" in plugins["assertions"]
        assert "ag1" in plugins["agents"]


class TestDecorators:
    def test_register_assertion_decorator(self):
        @register_assertion("assert_custom_test")
        def assert_custom_test(result):
            pass

        from vigil.plugins.registry import registry
        assert "assert_custom_test" in registry.assertions

    def test_register_agent_decorator(self):
        @register_agent("custom_agent_test")
        class CustomAgent:
            def run(self, input, **kwargs):
                return TestResult(output="test")

        from vigil.plugins.registry import registry
        assert "custom_agent_test" in registry.agents
