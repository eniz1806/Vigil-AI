"""Tests for core components."""

import pytest

from vigil.core.results import TestResult, Timer
from vigil.core.decorators import test as vigil_test
from vigil.core.config import VigilConfig, load_config


class TestTestResult:
    def test_basic(self):
        r = TestResult(output="hello")
        assert r.output == "hello"
        assert r.cost is None
        assert r.tokens_total is None
        assert str(r) == "hello"

    def test_with_tokens(self):
        r = TestResult(output="ok", tokens_input=10, tokens_output=20)
        assert r.tokens_total == 30

    def test_tokens_partial(self):
        r = TestResult(output="ok", tokens_input=10)
        assert r.tokens_total is None


class TestTimer:
    def test_measures_time(self):
        import time

        with Timer() as t:
            time.sleep(0.05)
        assert t.elapsed >= 0.04


class TestDecorators:
    def test_marks_function(self):
        @vigil_test()
        def my_test():
            return True

        assert my_test._vigil_test is True
        assert my_test._vigil_name == "my_test"

    def test_custom_name(self):
        @vigil_test(name="Custom Test")
        def my_test():
            pass

        assert my_test._vigil_name == "Custom Test"

    def test_tags(self):
        @vigil_test(tags=["slow", "api"])
        def my_test():
            pass

        assert my_test._vigil_tags == ["slow", "api"]

    def test_function_still_callable(self):
        @vigil_test()
        def my_test():
            return 42

        assert my_test() == 42


class TestConfig:
    def test_defaults(self):
        config = VigilConfig()
        assert config.cost_threshold == 0.05
        assert config.latency_threshold == 5.0
        assert config.semantic_threshold == 0.85

    def test_load_missing_file(self, tmp_path):
        config = load_config(tmp_path / "nonexistent.yaml")
        assert config.cost_threshold == 0.05

    def test_load_file(self, tmp_path):
        config_file = tmp_path / "vigil.yaml"
        config_file.write_text(
            "defaults:\n"
            "  cost_threshold: 0.10\n"
            "  latency_threshold: 3.0\n"
            "reporting:\n"
            "  verbose: true\n"
        )
        config = load_config(config_file)
        assert config.cost_threshold == 0.10
        assert config.latency_threshold == 3.0
        assert config.verbose is True
