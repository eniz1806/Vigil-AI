# LLM-as-Judge

The most powerful feature in Vigil. Instead of pattern matching, an LLM evaluates your agent's output against your criteria.

## Setup

```bash
pip install "vigil-ai[openai]"   # or vigil-ai[anthropic]
```

Set your API key:

```bash
export OPENAI_API_KEY=sk-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

## assert_quality

Grade output against a single set of criteria:

```python
from vigil import test, FunctionAgent, assert_quality

agent = FunctionAgent(my_agent)

@test()
def test_explanation():
    result = agent.run("Explain quantum computing to a 5-year-old")
    verdict = assert_quality(
        result,
        criteria="age-appropriate, accurate, under 100 words, uses simple analogies",
        threshold=0.7,
    )
    # verdict contains: {"score": 0.85, "reasoning": "..."}
```

## assert_rubric

Grade against multiple criteria individually:

```python
from vigil import test, FunctionAgent, assert_rubric

@test()
def test_article():
    result = agent.run("Write about climate change")
    verdict = assert_rubric(
        result,
        rubric={
            "accuracy": "All claims are factually correct",
            "clarity": "Easy to understand, no unnecessary jargon",
            "completeness": "Covers causes, effects, and solutions",
            "tone": "Professional and balanced",
        },
        threshold=0.7,
    )
    # verdict contains per-criterion scores
```

## With Context

Ground the evaluation in source material:

```python
assert_quality(
    result,
    criteria="Accurate summary of the source material",
    context="The original document text goes here...",
    threshold=0.8,
)
```

## Choosing a Provider

```python
# Auto-detect (checks OPENAI_API_KEY, then ANTHROPIC_API_KEY)
assert_quality(result, criteria="...")

# Explicit
assert_quality(result, criteria="...", provider="openai", model="gpt-4o-mini")
assert_quality(result, criteria="...", provider="anthropic", model="claude-haiku-4-5-20251001")
```

!!! warning
    LLM-as-judge assertions make API calls and cost money. Use a fast, cheap model (gpt-4o-mini, claude-haiku) for evaluation to keep costs low.
