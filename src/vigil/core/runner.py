"""Test runner — thin wrapper around pytest."""

from __future__ import annotations



def run(
    paths: list[str] | None = None,
    report: str | None = None,
    verbose: bool = False,
    parallel: int | None = None,
) -> int:
    """Run vigil tests using pytest as the engine.

    Args:
        paths: Files or directories to test. Defaults to current directory.
        report: Report format — "terminal", "json", or "html".
        verbose: Enable verbose output.
        parallel: Number of parallel workers. Requires pytest-xdist.

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

    if parallel is not None and parallel > 1:
        try:
            import xdist  # noqa: F401
            args.extend(["-n", str(parallel)])
        except ImportError:
            import warnings
            warnings.warn(
                "pytest-xdist is required for parallel execution. "
                "Install with: pip install pytest-xdist. Running sequentially.",
                stacklevel=2,
            )

    if paths:
        args.extend(paths)
    else:
        args.append(".")

    import pytest

    return pytest.main(args)
