"""Configuration loading."""

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


def load_config(path: Path | str | None = None) -> VigilConfig:
    """Load config from vigil.yaml, falling back to defaults."""
    if path is None:
        path = Path.cwd() / "vigil.yaml"
    else:
        path = Path(path)

    if not path.exists():
        return VigilConfig()

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
