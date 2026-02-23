# Quick Start

## 1. Initialize a project

```bash
vigil init
```

This creates:

- `vigil.yaml` — configuration file
- `tests/test_agent.py` — example test

Add `--ci` to also generate a GitHub Actions workflow.

## 2. Write a test

```python
from vigil import test, FunctionAgent, assert_contains

def my_agent(message: str) -> str:
    # Your agent logic here
    return "Hello! How can I help?"

agent = FunctionAgent(my_agent)

@test()
def test_greeting():
    result = agent.run("Hello!")
    assert_contains(result, "Hello")
```

## 3. Run tests

```bash
vigil run
```

Or use pytest directly:

```bash
pytest --vigil
```

## 4. Generate a report

```bash
# HTML report
vigil run --report html

# JSON (for CI pipelines)
vigil run --report json
```

## What's next?

- [Assertions](../guide/assertions.md) — all 11 built-in assertions
- [Agent Types](../guide/agents.md) — test functions, APIs, CLI tools
- [LLM-as-Judge](../guide/llm-judge.md) — use AI to evaluate AI
- [CI Integration](../guide/ci.md) — run in GitHub Actions
