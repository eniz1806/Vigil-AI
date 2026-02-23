"""Example — testing an OpenAI-based chatbot.

Requires: pip install vigil-eval[openai]
Set OPENAI_API_KEY in your environment.
"""

import os

import pytest

from vigil import (
    test,
    FunctionAgent,
    assert_contains,
    assert_cost_under,
    assert_latency_under,
    assert_semantic_match,
)


def openai_chat(message: str) -> dict:
    """Call OpenAI and return structured result."""
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        max_tokens=200,
    )
    usage = response.usage
    # Approximate cost for gpt-4o-mini
    cost = (usage.prompt_tokens * 0.15 + usage.completion_tokens * 0.6) / 1_000_000

    return {
        "output": response.choices[0].message.content,
        "cost": cost,
        "tokens_input": usage.prompt_tokens,
        "tokens_output": usage.completion_tokens,
        "model": response.model,
    }


# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)

agent = FunctionAgent(openai_chat)


@test()
def test_basic_response():
    result = agent.run("What is 2 + 2? Reply with just the number.")
    assert_contains(result, "4")
    assert_cost_under(result, 0.01)


@test()
def test_knowledge():
    result = agent.run("What programming language is known for its use in data science?")
    assert_semantic_match(result, "Python is widely used in data science", threshold=0.3)
    assert_latency_under(result, 10.0)


@test()
def test_cost_efficiency():
    result = agent.run("Say hello in one word.")
    assert_cost_under(result, 0.001)
