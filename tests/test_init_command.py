"""Tests for vigil init command."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from vigil.cli import main


class TestInitCommand:
    def test_creates_files(self, tmp_path: Path):
        runner = CliRunner()
        result = runner.invoke(main, ["init", "--dir", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "vigil.yaml").exists()
        assert (tmp_path / "tests" / "test_agent.py").exists()

    def test_creates_ci(self, tmp_path: Path):
        runner = CliRunner()
        result = runner.invoke(main, ["init", "--dir", str(tmp_path), "--ci"])
        assert result.exit_code == 0
        assert (tmp_path / ".github" / "workflows" / "ai-tests.yml").exists()

    def test_skips_existing(self, tmp_path: Path):
        # Create config first
        (tmp_path / "vigil.yaml").write_text("existing: true")
        runner = CliRunner()
        result = runner.invoke(main, ["init", "--dir", str(tmp_path)])
        assert result.exit_code == 0
        assert "skip" in result.output
        # Should not overwrite
        assert (tmp_path / "vigil.yaml").read_text() == "existing: true"
