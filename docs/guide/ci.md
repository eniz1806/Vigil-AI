# CI Integration

## GitHub Actions

### Using the Vigil Action

```yaml
name: AI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: vigil-ai/vigil@v1
        with:
          path: tests/
          report: terminal
```

### Manual setup

```yaml
name: AI Tests
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
```

### With API keys

```yaml
- run: vigil run
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### HTML report as artifact

```yaml
- run: vigil run --report html
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: vigil-report
    path: vigil-report.html
```

## Parallel execution

```bash
pip install "vigil-ai[parallel]"
vigil run --parallel 4
```

## JSON output for pipelines

```bash
vigil run --report json > results.json
```

The JSON output includes pass/fail status, cost totals, and per-test details — useful for custom dashboards or Slack notifications.
