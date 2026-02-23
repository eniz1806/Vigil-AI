# Configuration

Vigil looks for configuration in this order:

1. `vigil.yaml` in the current directory
2. `[tool.vigil]` in `pyproject.toml`
3. Default values

## vigil.yaml

```yaml
defaults:
  cost_threshold: 0.05
  latency_threshold: 5.0
  semantic_threshold: 0.85
  snapshot_dir: __snapshots__

reporting:
  format: terminal
  verbose: false
```

## pyproject.toml

```toml
[tool.vigil]
cost_threshold = 0.05
latency_threshold = 5.0
semantic_threshold = 0.85

[tool.vigil.reporting]
format = "terminal"
verbose = false
```

## Options

| Option | Default | Description |
|--------|---------|------------|
| `cost_threshold` | `0.05` | Default max cost per test ($) |
| `latency_threshold` | `5.0` | Default max latency per test (seconds) |
| `semantic_threshold` | `0.85` | Default semantic similarity threshold |
| `snapshot_dir` | `__snapshots__` | Directory for snapshot files |
| `report_format` | `terminal` | Default report format |
| `verbose` | `false` | Verbose output |
