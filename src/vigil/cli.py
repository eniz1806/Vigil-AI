"""Vigil CLI — command-line interface."""

from __future__ import annotations

import click

from vigil import __version__


@click.group()
@click.version_option(version=__version__, prog_name="vigil")
def main() -> None:
    """Vigil — The testing framework for AI agents."""


@main.command()
@click.argument("paths", nargs=-1)
@click.option("--report", type=click.Choice(["terminal", "json", "html"]), default="terminal")
@click.option("-v", "--verbose", is_flag=True)
def run(paths: tuple[str, ...], report: str, verbose: bool) -> None:
    """Run AI agent tests."""
    from vigil.core.runner import run as run_tests

    exit_code = run_tests(
        paths=list(paths) if paths else None,
        report=report,
        verbose=verbose,
    )
    raise SystemExit(exit_code)


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
