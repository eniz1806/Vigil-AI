# Vigil

**The testing framework for AI agents. Fast, framework-agnostic, CI-ready.**

Vigil makes testing AI agents and LLM applications as easy as writing pytest tests. Write tests in plain Python, run them in CI, catch regressions before production.

## Why Vigil?

- **40% of agentic AI projects** risk cancellation due to reliability issues
- **Only 52% of teams** use any form of evaluation
- Existing tools are framework-specific, complex, or disconnected from CI/CD

Vigil fixes this by giving you **pytest-like simplicity** for AI testing.

## Quick Example

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

## Features

| Feature | Description |
|---------|------------|
| **11 assertions** | Content, cost, latency, semantic, hallucination, LLM-as-judge |
| **3 agent types** | Python functions, HTTP APIs, CLI tools |
| **Snapshot testing** | Save golden outputs, detect regressions |
| **Cost tracking** | Auto-calculate costs for OpenAI, Anthropic, Google, DeepSeek |
| **Plugin system** | Extend with custom assertions, agents, reporters |
| **CI-ready** | Exit codes, JSON/HTML reports, GitHub Action |
| **Parallel execution** | Run tests concurrently with `--parallel` |
| **Async support** | Test async agents natively |

## Install

```bash
pip install vigil-eval
```
