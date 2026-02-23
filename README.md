<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/logo-with-text.svg">
    <img alt="Vigil" src="assets/logo-with-text.svg" width="480">
  </picture>
</p>

<p align="center">
  <strong>The testing framework for AI agents. Fast, framework-agnostic, CI-ready.</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#features">Features</a> &middot;
  <a href="#assertions">Assertions</a> &middot;
  <a href="#agent-types">Agent Types</a> &middot;
  <a href="#ci-integration">CI Integration</a>
</p>

---

Vigil makes testing AI agents and LLM applications as easy as writing pytest tests. Write tests in plain Python, run them in CI, catch regressions before production.

```bash
pip install vigil-ai
```

## Quick Start

```python
from vigil import test, FunctionAgent, assert_contains, assert_cost_under

# Wrap any function as an agent under test
agent = FunctionAgent(my_chatbot)

@test()
def test_greeting():
    result = agent.run("Hello!")
    assert_contains(result, "hello")
    assert_cost_under(result, 0.01)

@test()
def test_knowledge():
    result = agent.run("What is Python?")
    assert_contains(result, "programming")
```

Run your tests:

```bash
vigil run
# or
pytest --vigil
```

## Features

- **Framework-agnostic** — test any agent: Python functions, HTTP APIs, CLI tools
- **Rich assertions** — semantic matching, hallucination detection, cost/latency checks
- **Snapshot testing** — save golden outputs, detect regressions automatically
- **CI-ready** — exit codes, JSON reports, GitHub Actions integration
- **Zero config** — works out of the box, configure when you need to
- **Built on pytest** — use everything you already know

## Assertions

| Assertion | What it checks |
|-----------|---------------|
| `assert_contains(result, text)` | Output contains expected text |
| `assert_not_contains(result, text)` | Output does not contain text |
| `assert_json_valid(result)` | Output is valid JSON |
| `assert_matches_regex(result, pattern)` | Output matches regex pattern |
| `assert_cost_under(result, max_dollars)` | API cost below threshold |
| `assert_tokens_under(result, max_tokens)` | Token usage below threshold |
| `assert_latency_under(result, max_seconds)` | Response time below threshold |
| `assert_semantic_match(result, ref, threshold)` | Semantically similar to reference |
| `assert_no_hallucination(result, context)` | Output grounded in provided context |

## Agent Types

```python
from vigil import FunctionAgent, HTTPAgent, CLIAgent

# Test a Python function
agent = FunctionAgent(my_function)

# Test an HTTP endpoint
agent = HTTPAgent("http://localhost:8000/chat")

# Test a CLI tool
agent = CLIAgent("python my_agent.py")
```

## Snapshot Testing

```python
from vigil import test, FunctionAgent
from vigil.snapshots import snapshot

agent = FunctionAgent(my_agent)

@test()
def test_output_stable():
    result = agent.run("Summarize this document")
    snapshot(result, name="summary_output")
```

Update snapshots when outputs intentionally change:

```bash
vigil snapshot update
```

## CI Integration

```yaml
# .github/workflows/ai-tests.yml
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
      - run: vigil run --report json > results.json
```

## Configuration

Create a `vigil.yaml` in your project root:

```yaml
defaults:
  cost_threshold: 0.05
  latency_threshold: 5.0
  semantic_threshold: 0.85

reporting:
  format: terminal
  verbose: true
```

## License

Apache 2.0
