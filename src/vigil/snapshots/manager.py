"""Snapshot manager — save, compare, and update golden outputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from vigil.core.results import TestResult

# Global flag set by CLI when running `vigil snapshot update`
_UPDATE_SNAPSHOTS = False


def _get_snapshot_dir() -> Path:
    return Path.cwd() / "__snapshots__"


def _snapshot_path(name: str, snapshot_dir: Path | None = None) -> Path:
    d = snapshot_dir or _get_snapshot_dir()
    d.mkdir(parents=True, exist_ok=True)
    safe_name = name.replace("/", "_").replace(" ", "_")
    return d / f"{safe_name}.json"


class SnapshotManager:
    """Manages snapshot files for golden output testing."""

    def __init__(self, snapshot_dir: Path | str | None = None) -> None:
        self.snapshot_dir = Path(snapshot_dir) if snapshot_dir else _get_snapshot_dir()

    def save(self, name: str, output: str, metadata: dict[str, Any] | None = None) -> Path:
        path = _snapshot_path(name, self.snapshot_dir)
        data = {
            "output": output,
            "hash": hashlib.sha256(output.encode()).hexdigest()[:16],
            "metadata": metadata or {},
        }
        path.write_text(json.dumps(data, indent=2) + "\n")
        return path

    def load(self, name: str) -> dict[str, Any] | None:
        path = _snapshot_path(name, self.snapshot_dir)
        if not path.exists():
            return None
        return json.loads(path.read_text())

    def compare(self, name: str, current_output: str) -> tuple[bool, str | None]:
        """Compare current output to snapshot.

        Returns (matches, previous_output).
        """
        existing = self.load(name)
        if existing is None:
            return True, None  # First run, no comparison needed

        previous = existing["output"]
        current_hash = hashlib.sha256(current_output.encode()).hexdigest()[:16]
        return current_hash == existing["hash"], previous

    def list_snapshots(self) -> list[str]:
        if not self.snapshot_dir.exists():
            return []
        return [p.stem for p in self.snapshot_dir.glob("*.json")]


# Convenience function for use in tests
_default_manager: SnapshotManager | None = None


def snapshot(
    result: TestResult | str,
    name: str,
    threshold: float | None = None,
) -> None:
    """Assert that output matches the saved snapshot, or save it if new.

    Args:
        result: The agent output to snapshot.
        name: Name for this snapshot.
        threshold: Optional similarity threshold for fuzzy matching (not yet implemented).
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = SnapshotManager()

    output = result.output if isinstance(result, TestResult) else result

    if _UPDATE_SNAPSHOTS:
        _default_manager.save(name, output)
        return

    existing = _default_manager.load(name)
    if existing is None:
        # First run — save the snapshot
        _default_manager.save(name, output)
        return

    matches, previous = _default_manager.compare(name, output)
    if not matches:
        raise AssertionError(
            f"Snapshot '{name}' has changed.\n"
            f"Previous: '{previous[:200]}{'...' if previous and len(previous) > 200 else ''}'\n"
            f"Current:  '{output[:200]}{'...' if len(output) > 200 else ''}'\n"
            f"Run 'vigil snapshot update' to accept the new output."
        )
