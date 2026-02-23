# Assertions

Vigil provides 11 built-in assertions across 5 categories.

## Content

```python
from vigil import assert_contains, assert_not_contains, assert_json_valid, assert_matches_regex

# Check text is present
assert_contains(result, "expected text")
assert_contains(result, "hello", case_sensitive=False)

# Check text is absent
assert_not_contains(result, "error")

# Validate JSON output
data = assert_json_valid(result)  # returns parsed dict

# Match regex
match = assert_matches_regex(result, r"code: (\d+)")
```

## Cost

```python
from vigil import assert_cost_under, assert_tokens_under

# Check API cost
assert_cost_under(result, max_dollars=0.05)

# Check token usage
assert_tokens_under(result, max_tokens=1000)
```

!!! note
    Cost and token assertions require the agent to return cost/token data in the `TestResult`.

## Latency

```python
from vigil import assert_latency_under

assert_latency_under(result, max_seconds=2.0)
```

## Semantic Similarity

```python
from vigil import assert_semantic_match

# Auto-detects best method available
assert_semantic_match(result, "Python is a programming language", threshold=0.7)

# Force a specific method
assert_semantic_match(result, reference, method="word_overlap")  # no deps
assert_semantic_match(result, reference, method="cosine")        # needs numpy
assert_semantic_match(result, reference, method="embedding")     # needs openai
```

## Quality (Hallucination Detection)

```python
from vigil import assert_no_hallucination

context = "Python was created by Guido van Rossum in 1991."
assert_no_hallucination(result, context=context, threshold=0.5)
```

## LLM-as-Judge

See [LLM-as-Judge](llm-judge.md) for the most powerful assertion.
