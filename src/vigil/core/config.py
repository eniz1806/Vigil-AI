"""Configuration loading — supports vigil.yaml and pyproject.toml [tool.vigil]."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class VigilConfig:
    """Project-level vigil configuration."""

    cost_threshold: float = 0.05
    latency_threshold: float = 5.0
    semantic_threshold: float = 0.85
    report_format: str = "terminal"
    verbose: bool = False
    snapshot_dir: str = "__snapshots__"
    extra: dict[str, Any] = field(default_factory=dict)


def _load_from_yaml(path: Path) -> VigilConfig | None:
    """Load config from vigil.yaml."""
    if not path.exists():
        return None

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    defaults = raw.get("defaults", {})
    reporting = raw.get("reporting", {})

    return VigilConfig(
        cost_threshold=defaults.get("cost_threshold", 0.05),
        latency_threshold=defaults.get("latency_threshold", 5.0),
        semantic_threshold=defaults.get("semantic_threshold", 0.85),
        report_format=reporting.get("format", "terminal"),
        verbose=reporting.get("verbose", False),
        snapshot_dir=defaults.get("snapshot_dir", "__snapshots__"),
        extra=raw,
    )


def _load_from_pyproject(path: Path) -> VigilConfig | None:
    """Load config from pyproject.toml [tool.vigil]."""
    if not path.exists():
        return None

    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            return None

    with open(path, "rb") as f:
        data = tomllib.load(f)

    vigil_config = data.get("tool", {}).get("vigil", None)
    if vigil_config is None:
        return None

    defaults = vigil_config.get("defaults", vigil_config)
    reporting = vigil_config.get("reporting", {})

    return VigilConfig(
        cost_threshold=defaults.get("cost_threshold", 0.05),
        latency_threshold=defaults.get("latency_threshold", 5.0),
        semantic_threshold=defaults.get("semantic_threshold", 0.85),
        report_format=reporting.get("format", "terminal"),
        verbose=reporting.get("verbose", False),
        snapshot_dir=defaults.get("snapshot_dir", "__snapshots__"),
        extra=vigil_config,
    )


def load_config(path: Path | str | None = None) -> VigilConfig:
    """Load config with priority: explicit path > vigil.yaml > pyproject.toml > defaults.

    Search order:
        1. Explicit path (if provided)
        2. vigil.yaml in current directory
        3. [tool.vigil] in pyproject.toml in current directory
        4. Default values
    """
    if path is not None:
        p = Path(path)
        if p.suffix in (".yaml", ".yml"):
            cfg = _load_from_yaml(p)
        elif p.name == "pyproject.toml":
            cfg = _load_from_pyproject(p)
        else:
            cfg = _load_from_yaml(p)
        return cfg or VigilConfig()

    # Auto-discover
    cwd = Path.cwd()

    cfg = _load_from_yaml(cwd / "vigil.yaml")
    if cfg is not None:
        return cfg

    cfg = _load_from_pyproject(cwd / "pyproject.toml")
    if cfg is not None:
        return cfg

    return VigilConfig()
