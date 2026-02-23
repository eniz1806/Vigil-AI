# Snapshot Testing

Save golden outputs and detect when your agent's behavior changes.

## Basic Usage

```python
from vigil import test, FunctionAgent
from vigil.snapshots import snapshot

agent = FunctionAgent(my_agent)

@test()
def test_summary():
    result = agent.run("Summarize this document")
    snapshot(result, name="summary_output")
```

**First run:** Saves the output to `__snapshots__/summary_output.json`.

**Subsequent runs:** Compares against the saved snapshot. Fails if the output changed.

## Updating Snapshots

When outputs intentionally change:

```bash
vigil snapshot update
```

## Managing Snapshots

```bash
# List all snapshots
vigil snapshot list
```

## Snapshot Directory

By default, snapshots are saved to `__snapshots__/`. Configure in `vigil.yaml`:

```yaml
defaults:
  snapshot_dir: my_snapshots
```

!!! tip
    Add `__snapshots__/` to `.gitignore` if you don't want to track them, or commit them if you want to detect regressions in CI.
