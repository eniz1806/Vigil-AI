"""Vigil pytest plugin — integrates Vigil with pytest."""

from __future__ import annotations

import time
from typing import Any

import pytest

from vigil.core.config import load_config
from vigil.reporting.terminal import TerminalReporter

# Module-level state (shared across hooks)
_reporter: TerminalReporter | None = None
_report_format: str = "terminal"
_test_start_times: dict[str, float] = {}


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("vigil", "Vigil AI testing")
    group.addoption(
        "--vigil-report",
        type=str,
        default=None,
        choices=["terminal", "json", "html"],
        help="Vigil report format.",
    )
    group.addoption(
        "--vigil-config",
        type=str,
        default=None,
        help="Path to vigil.yaml config file.",
    )


def pytest_configure(config: Any) -> None:
    global _reporter, _report_format
    verbose = config.getoption("verbose", default=0) > 0
    _report_format = config.getoption("--vigil-report", default=None) or "terminal"
    _reporter = TerminalReporter(verbose=verbose)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: Any) -> None:
    _test_start_times[item.nodeid] = time.perf_counter()


def pytest_runtest_logreport(report: Any) -> None:
    if report.when != "call" or _reporter is None:
        return

    duration = report.duration
    passed = report.passed
    error = None
    if report.failed:
        error = str(report.longreprtext)[:500] if hasattr(report, "longreprtext") else "Failed"

    _reporter.add_result(
        name=report.nodeid,
        passed=passed,
        duration=duration,
        error=error,
    )


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    if _reporter is None or not _reporter.results:
        return

    if _report_format == "terminal":
        _reporter.render()
    elif _report_format == "html":
        from vigil.reporting.html import HTMLReporter

        html = HTMLReporter()
        html.results = _reporter.results
        path = html.render()
        _reporter.console.print(f"\nHTML report saved to: {path}")
    elif _report_format == "json":
        from vigil.reporting.html import HTMLReporter

        html = HTMLReporter()
        html.results = _reporter.results
        print(html.to_json())


@pytest.fixture
def vigil_config() -> Any:
    """Fixture that provides the Vigil configuration."""
    return load_config()
