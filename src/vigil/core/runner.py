"""Test runner — thin wrapper around pytest."""

from __future__ import annotations

import sys
from pathlib import Path


def run(
    paths: list[str] | None = None,
    report: str | None = None,
    verbose: bool = False,
) -> int:
    """Run vigil tests using pytest as the engine.

    Args:
        paths: Files or directories to test. Defaults to current directory.
        report: Report format — "terminal", "json", or "html".
        verbose: Enable verbose output.

    Returns:
        Exit code (0 = all passed).
    """
    args = ["-p", "vigil.plugins.pytest_plugin"]

    if verbose:
        args.append("-v")

    if report == "json":
        args.extend(["--vigil-report", "json"])
    elif report == "html":
        args.extend(["--vigil-report", "html"])

    if paths:
        args.extend(paths)
    else:
        args.append(".")

    import pytest

    return pytest.main(args)
