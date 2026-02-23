"""Tests for config loading including pyproject.toml support."""

import pytest
from pathlib import Path

from vigil.core.config import VigilConfig, load_config


class TestPyprojectConfig:
    def test_load_from_pyproject(self, tmp_path: Path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.vigil]\n'
            'cost_threshold = 0.10\n'
            'latency_threshold = 3.0\n'
            '\n'
            '[tool.vigil.reporting]\n'
            'format = "json"\n'
            'verbose = true\n'
        )
        config = load_config(pyproject)
        assert config.cost_threshold == 0.10
        assert config.latency_threshold == 3.0
        assert config.report_format == "json"
        assert config.verbose is True

    def test_yaml_takes_priority(self, tmp_path: Path, monkeypatch):
        # Create both files
        yaml_file = tmp_path / "vigil.yaml"
        yaml_file.write_text(
            "defaults:\n"
            "  cost_threshold: 0.20\n"
        )
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.vigil]\n'
            'cost_threshold = 0.50\n'
        )

        monkeypatch.chdir(tmp_path)
        config = load_config()
        # YAML should win
        assert config.cost_threshold == 0.20

    def test_fallback_to_pyproject(self, tmp_path: Path, monkeypatch):
        # Only pyproject.toml exists
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.vigil]\n'
            'cost_threshold = 0.30\n'
        )

        monkeypatch.chdir(tmp_path)
        config = load_config()
        assert config.cost_threshold == 0.30

    def test_no_vigil_section(self, tmp_path: Path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[tool.ruff]\n'
            'line-length = 100\n'
        )
        config = load_config(pyproject)
        # Should return defaults
        assert config.cost_threshold == 0.05

    def test_defaults_when_nothing_exists(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = load_config()
        assert config.cost_threshold == 0.05
        assert config.latency_threshold == 5.0
