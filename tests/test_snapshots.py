"""Tests for snapshot manager."""

import pytest
from pathlib import Path

from vigil.core.results import TestResult
from vigil.snapshots.manager import SnapshotManager


@pytest.fixture
def snap_dir(tmp_path: Path) -> Path:
    return tmp_path / "snapshots"


@pytest.fixture
def manager(snap_dir: Path) -> SnapshotManager:
    return SnapshotManager(snap_dir)


class TestSnapshotManager:
    def test_save_and_load(self, manager: SnapshotManager):
        manager.save("test1", "hello world")
        data = manager.load("test1")
        assert data is not None
        assert data["output"] == "hello world"

    def test_load_nonexistent(self, manager: SnapshotManager):
        assert manager.load("nonexistent") is None

    def test_compare_match(self, manager: SnapshotManager):
        manager.save("test1", "hello world")
        matches, _ = manager.compare("test1", "hello world")
        assert matches is True

    def test_compare_mismatch(self, manager: SnapshotManager):
        manager.save("test1", "hello world")
        matches, previous = manager.compare("test1", "goodbye world")
        assert matches is False
        assert previous == "hello world"

    def test_compare_first_run(self, manager: SnapshotManager):
        matches, previous = manager.compare("new_test", "some output")
        assert matches is True
        assert previous is None

    def test_list_snapshots(self, manager: SnapshotManager):
        manager.save("alpha", "a")
        manager.save("beta", "b")
        snapshots = manager.list_snapshots()
        assert set(snapshots) == {"alpha", "beta"}

    def test_list_empty(self, manager: SnapshotManager):
        assert manager.list_snapshots() == []

    def test_overwrite(self, manager: SnapshotManager):
        manager.save("test1", "version 1")
        manager.save("test1", "version 2")
        data = manager.load("test1")
        assert data["output"] == "version 2"
