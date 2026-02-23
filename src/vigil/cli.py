"""Vigil CLI — command-line interface."""

from __future__ import annotations

from pathlib import Path

import click

from vigil import __version__


_INIT_CONFIG = """# Vigil configuration
defaults:
  cost_threshold: 0.05
  latency_threshold: 5.0
  semantic_threshold: 0.85

reporting:
  format: terminal
  verbose: false
"""

_INIT_TEST = '''"""Example Vigil test — replace with your own agent."""

from vigil import test, FunctionAgent, assert_contains


# Replace this with your real agent
def my_agent(message: str) -> str:
    return f"You said: {message}"


agent = FunctionAgent(my_agent)


@test()
def test_basic_response():
    result = agent.run("Hello!")
    assert_contains(result, "Hello")


@test()
def test_no_errors():
    result = agent.run("Tell me something")
    assert_contains(result, "Tell me something")
'''

_INIT_CI = """name: AI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install vigil-ai
      - run: vigil run
"""


@click.group()
@click.version_option(version=__version__, prog_name="vigil")
def main() -> None:
    """Vigil — The testing framework for AI agents."""


@main.command()
@click.argument("paths", nargs=-1)
@click.option("--report", type=click.Choice(["terminal", "json", "html"]), default="terminal")
@click.option("-v", "--verbose", is_flag=True)
@click.option("-p", "--parallel", type=int, default=None, help="Number of parallel workers.")
def run(paths: tuple[str, ...], report: str, verbose: bool, parallel: int | None) -> None:
    """Run AI agent tests."""
    from vigil.core.runner import run as run_tests

    exit_code = run_tests(
        paths=list(paths) if paths else None,
        report=report,
        verbose=verbose,
        parallel=parallel,
    )
    raise SystemExit(exit_code)


@main.command()
@click.option("--dir", "directory", default=".", help="Directory to initialize.")
@click.option("--ci", is_flag=True, help="Also generate GitHub Actions workflow.")
def init(directory: str, ci: bool) -> None:
    """Initialize a new Vigil project with config and example test."""
    base = Path(directory).resolve()

    # vigil.yaml
    config_path = base / "vigil.yaml"
    if config_path.exists():
        click.echo(f"  skip  {config_path} (already exists)")
    else:
        config_path.write_text(_INIT_CONFIG)
        click.echo(f"  create  {config_path}")

    # tests directory
    tests_dir = base / "tests"
    tests_dir.mkdir(exist_ok=True)

    test_path = tests_dir / "test_agent.py"
    if test_path.exists():
        click.echo(f"  skip  {test_path} (already exists)")
    else:
        test_path.write_text(_INIT_TEST)
        click.echo(f"  create  {test_path}")

    # CI workflow
    if ci:
        workflows_dir = base / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        ci_path = workflows_dir / "ai-tests.yml"
        if ci_path.exists():
            click.echo(f"  skip  {ci_path} (already exists)")
        else:
            ci_path.write_text(_INIT_CI)
            click.echo(f"  create  {ci_path}")

    click.echo()
    click.echo("Vigil project initialized! Next steps:")
    click.echo("  1. Edit tests/test_agent.py with your agent")
    click.echo("  2. Run: vigil run")


@main.group()
def snapshot() -> None:
    """Manage test snapshots."""


@snapshot.command("update")
@click.argument("names", nargs=-1)
def snapshot_update(names: tuple[str, ...]) -> None:
    """Update snapshots to accept current outputs."""
    import vigil.snapshots.manager as mgr

    mgr._UPDATE_SNAPSHOTS = True
    click.echo("Snapshot update mode enabled. Run your tests to update snapshots.")

    from vigil.core.runner import run as run_tests
    exit_code = run_tests()
    mgr._UPDATE_SNAPSHOTS = False

    if exit_code == 0:
        click.echo("Snapshots updated successfully.")
    raise SystemExit(exit_code)


@snapshot.command("list")
def snapshot_list() -> None:
    """List all saved snapshots."""
    from vigil.snapshots.manager import SnapshotManager

    manager = SnapshotManager()
    snapshots = manager.list_snapshots()
    if not snapshots:
        click.echo("No snapshots found.")
        return
    click.echo(f"Found {len(snapshots)} snapshot(s):")
    for name in sorted(snapshots):
        click.echo(f"  - {name}")


@main.command()
@click.argument("paths", nargs=-1)
@click.option("-o", "--output", default="vigil-report.html")
def report(paths: tuple[str, ...], output: str) -> None:
    """Generate an HTML test report."""
    click.echo(f"Generating report to {output}...")
    from vigil.core.runner import run as run_tests

    exit_code = run_tests(
        paths=list(paths) if paths else None,
        report="html",
    )
    click.echo(f"Report saved to {output}")
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
