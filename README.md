<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/eniz1806/Vigil-AI/main/assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eniz1806/Vigil-AI/main/assets/logo-with-text.svg">
    <img alt="Vigil" src="https://raw.githubusercontent.com/eniz1806/Vigil-AI/main/assets/logo-with-text.svg" width="480">
  </picture>
</p>

<p align="center">
  <strong>The testing framework for AI agents. Fast, framework-agnostic, CI-ready.</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/vigil-eval/"><img src="https://img.shields.io/pypi/v/vigil-eval?color=6366F1&label=PyPI" alt="PyPI"></a>
  <a href="https://pypi.org/project/vigil-eval/"><img src="https://img.shields.io/pypi/pyversions/vigil-eval?color=6366F1" alt="Python"></a>
  <a href="https://github.com/eniz1806/Vigil-AI/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-6366F1" alt="License"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#features">Features</a> &middot;
  <a href="#assertions">Assertions</a> &middot;
  <a href="#llm-as-judge">LLM-as-Judge</a> &middot;
  <a href="#ci-integration">CI Integration</a> &middot;
  <a href="https://pypi.org/project/vigil-eval/">PyPI</a>
</p>

---

## Why Vigil?

**40% of agentic AI projects** risk cancellation due to reliability issues. Only **52% of teams** run any form of evaluation. The rest ship and pray.

Existing tools are either framework-specific, complex to set up, or disconnected from CI/CD. There's no "pytest for AI."

**Vigil changes that.** Write AI tests in plain Python. Run them in CI. Catch regressions before production.

```bash
pip install vigil-eval
```

## Quick Start

```python
from vigil import test, FunctionAgent, assert_contains, assert_cost_under

agent = FunctionAgent(my_chatbot)

@test()
def test_greeting():
    result = agent.run("Hello!")
    assert_contains(result, "hello")
    assert_cost_under(result, 0.01)
```

```bash
vigil run
```

That's it. No config files, no setup, no boilerplate.

## Features

| Feature | Description |
|---------|------------|
| **11+ assertions** | Content, cost, latency, semantic, hallucination, LLM-as-judge |
| **3 agent types** | Python functions, HTTP APIs, CLI tools |
| **LLM-as-judge** | Use GPT/Claude to grade your agent's output against criteria |
| **Snapshot testing** | Save golden outputs, detect regressions automatically |
| **Cost tracking** | Auto-calculate API costs for 20+ models across 4 providers |
| **Plugin system** | Extend with custom assertions, agents, and reporters |
| **CI-ready** | Exit codes, JSON/HTML reports, GitHub Action included |
| **Parallel execution** | Run tests concurrently with `--parallel` |
| **Async support** | Test async agents natively |
| **Zero config** | Works out of the box, configure when you need to |
| **Built on pytest** | Use everything you already know |

## Assertions

```python
from vigil import (
    assert_contains,          # output contains expected text
    assert_not_contains,      # output does not contain text
    assert_json_valid,        # output is valid JSON
    assert_matches_regex,     # output matches regex pattern
    assert_cost_under,        # API cost below threshold
    assert_tokens_under,      # token usage below limit
    assert_latency_under,     # response time below threshold
    assert_semantic_match,    # semantically similar to reference
    assert_no_hallucination,  # output grounded in provided context
    assert_quality,           # LLM grades output against criteria
    assert_rubric,            # LLM grades against multiple criteria
)
```

## LLM-as-Judge

The most powerful feature in Vigil. Instead of pattern matching, an LLM evaluates your agent's output:

```python
from vigil import test, FunctionAgent, assert_quality, assert_rubric

agent = FunctionAgent(my_agent)

@test()
def test_explanation():
    result = agent.run("Explain quantum computing to a 5-year-old")
    assert_quality(
        result,
        criteria="age-appropriate, accurate, under 100 words, uses simple analogies",
        threshold=0.7,
    )

@test()
def test_article():
    result = agent.run("Write about climate change")
    assert_rubric(
        result,
        rubric={
            "accuracy": "All claims are factually correct",
            "clarity": "Easy to understand, no jargon",
            "completeness": "Covers causes, effects, and solutions",
        },
        threshold=0.7,
    )
```

Works with OpenAI and Anthropic. Auto-detects your API key.

## Agent Types

```python
from vigil import FunctionAgent, HTTPAgent, CLIAgent

# Test a Python function (sync or async)
agent = FunctionAgent(my_function)

# Test an HTTP endpoint
agent = HTTPAgent("http://localhost:8000/chat")

# Test a CLI tool
agent = CLIAgent("python my_agent.py")
```

## Cost Tracking

Vigil auto-calculates API costs for 20+ models:

```python
from vigil import FunctionAgent, assert_cost_under
from vigil.cost import enrich_result

def my_agent(msg):
    return {"output": "Hello!", "model": "gpt-4o-mini", "tokens_input": 50, "tokens_output": 100}

result = FunctionAgent(my_agent).run("Hi")
enrich_result(result)
print(result.cost)  # Auto-calculated from pricing table

assert_cost_under(result, 0.01)
```

Supports OpenAI, Anthropic, Google, and DeepSeek models.

## Snapshot Testing

Save golden outputs and detect when your agent's behavior drifts:

```python
from vigil import test, FunctionAgent
from vigil.snapshots import snapshot

@test()
def test_output_stable():
    result = FunctionAgent(my_agent).run("Summarize this document")
    snapshot(result, name="summary_output")
```

```bash
# First run: saves snapshot. Next runs: compares against it.
vigil run

# Accept new outputs when they intentionally change
vigil snapshot update
```

## CI Integration

### GitHub Actions

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
      - run: pip install vigil-eval
      - run: vigil run
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Reports

```bash
vigil run --report json > results.json   # For pipelines
vigil run --report html                  # Standalone HTML report
```

### Parallel Execution

```bash
pip install "vigil-eval[parallel]"
vigil run --parallel 4
```

## Configuration

Works with zero config. When you need it, create `vigil.yaml`:

```yaml
defaults:
  cost_threshold: 0.05
  latency_threshold: 5.0
  semantic_threshold: 0.85

reporting:
  format: terminal
  verbose: true
```

Or add to your existing `pyproject.toml`:

```toml
[tool.vigil]
cost_threshold = 0.05
latency_threshold = 5.0
```

## Plugins

Extend Vigil with custom assertions, agents, and reporters:

```python
from vigil.plugins import register_assertion

@register_assertion("assert_polite")
def assert_polite(result, **kwargs):
    polite_words = ["please", "thank", "sorry", "appreciate"]
    if not any(word in result.output.lower() for word in polite_words):
        raise AssertionError("Output is not polite")
```

Plugins are auto-discovered via Python entry points.

## Install

```bash
pip install vigil-eval                    # Core
pip install "vigil-eval[openai]"          # + OpenAI (LLM-as-judge, embeddings)
pip install "vigil-eval[anthropic]"       # + Anthropic
pip install "vigil-eval[all]"             # Everything
```

## License

Apache 2.0
