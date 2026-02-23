"""LLM-as-judge assertions — use an LLM to evaluate agent outputs.

This is the most powerful assertion in Vigil. Instead of pattern matching,
an LLM grades the output against your criteria.

Requires: pip install vigil-eval[openai] or vigil-eval[anthropic]
"""

from __future__ import annotations

import json
import os
from typing import Any

from vigil.core.results import TestResult

_JUDGE_PROMPT = """You are an AI output quality judge. Evaluate the following output against the given criteria.

CRITERIA:
{criteria}

OUTPUT TO EVALUATE:
{output}

{context_section}

Score the output from 0.0 to 1.0 where:
- 0.0 = completely fails the criteria
- 0.5 = partially meets the criteria
- 1.0 = perfectly meets the criteria

Respond with ONLY a JSON object in this exact format:
{{"score": <float>, "reasoning": "<brief explanation>"}}"""

_JUDGE_PROMPT_WITH_RUBRIC = """You are an AI output quality judge. Evaluate the following output against each criterion in the rubric.

RUBRIC:
{rubric}

OUTPUT TO EVALUATE:
{output}

{context_section}

Score each criterion from 0.0 to 1.0. Then compute the overall score as the average.

Respond with ONLY a JSON object in this exact format:
{{"scores": {{"<criterion>": <float>, ...}}, "overall": <float>, "reasoning": "<brief explanation>"}}"""


def _get_output(result: TestResult | str) -> str:
    if isinstance(result, TestResult):
        return result.output
    return result


def _call_openai(prompt: str, model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI is required for LLM-as-judge. Install with: pip install vigil-eval[openai]"
        )
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    return response.choices[0].message.content


def _call_anthropic(prompt: str, model: str) -> str:
    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError(
            "Anthropic is required for LLM-as-judge. Install with: pip install vigil-eval[anthropic]"
        )
    client = Anthropic()
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=500,
    )
    return response.content[0].text


def _call_judge(prompt: str, provider: str, model: str) -> str:
    if provider == "openai":
        return _call_openai(prompt, model)
    elif provider == "anthropic":
        return _call_anthropic(prompt, model)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'anthropic'.")


def _detect_provider() -> tuple[str, str]:
    """Auto-detect which LLM provider is available."""
    if os.environ.get("OPENAI_API_KEY"):
        return "openai", "gpt-4o-mini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic", "claude-haiku-4-5-20251001"
    raise RuntimeError(
        "No LLM provider found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY "
        "to use LLM-as-judge assertions."
    )


def _parse_judge_response(response: str) -> dict[str, Any]:
    """Parse the JSON response from the judge LLM."""
    text = response.strip()
    # Handle markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON in the response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        raise ValueError(f"Could not parse judge response as JSON: {text[:200]}")


def assert_quality(
    result: TestResult | str,
    criteria: str,
    threshold: float = 0.7,
    context: str | None = None,
    provider: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Assert that the output meets quality criteria, as judged by an LLM.

    Args:
        result: The agent output to evaluate.
        criteria: Description of what "good" looks like.
        threshold: Minimum score (0.0 to 1.0).
        context: Optional context the output should be based on.
        provider: "openai" or "anthropic". Auto-detected if not set.
        model: Model to use as judge. Defaults to a fast, cheap model.

    Returns:
        The judge's full response dict with score and reasoning.

    Example:
        result = agent.run("Explain quantum computing to a child")
        assert_quality(result, criteria="age-appropriate, accurate, under 100 words")
    """
    output = _get_output(result)

    if provider is None or model is None:
        auto_provider, auto_model = _detect_provider()
        provider = provider or auto_provider
        model = model or auto_model

    context_section = f"CONTEXT (output should be based on this):\n{context}" if context else ""

    prompt = _JUDGE_PROMPT.format(
        criteria=criteria,
        output=output,
        context_section=context_section,
    )

    response = _call_judge(prompt, provider, model)
    parsed = _parse_judge_response(response)
    score = float(parsed.get("score", 0))

    if score < threshold:
        raise AssertionError(
            f"Quality score {score:.2f} below threshold {threshold:.2f}\n"
            f"Criteria: {criteria}\n"
            f"Reasoning: {parsed.get('reasoning', 'N/A')}"
        )

    return parsed


def assert_rubric(
    result: TestResult | str,
    rubric: dict[str, str],
    threshold: float = 0.7,
    context: str | None = None,
    provider: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """Assert that the output passes a multi-criteria rubric, as judged by an LLM.

    Args:
        result: The agent output to evaluate.
        rubric: Dict of {criterion_name: description}.
        threshold: Minimum overall score (0.0 to 1.0).
        context: Optional source context.
        provider: "openai" or "anthropic".
        model: Judge model.

    Returns:
        The judge's full response with per-criterion scores.

    Example:
        assert_rubric(result, rubric={
            "accuracy": "Information is factually correct",
            "clarity": "Easy to understand, no jargon",
            "completeness": "Covers all key points",
        })
    """
    output = _get_output(result)

    if provider is None or model is None:
        auto_provider, auto_model = _detect_provider()
        provider = provider or auto_provider
        model = model or auto_model

    rubric_text = "\n".join(f"- {k}: {v}" for k, v in rubric.items())
    context_section = f"CONTEXT (output should be based on this):\n{context}" if context else ""

    prompt = _JUDGE_PROMPT_WITH_RUBRIC.format(
        rubric=rubric_text,
        output=output,
        context_section=context_section,
    )

    response = _call_judge(prompt, provider, model)
    parsed = _parse_judge_response(response)
    overall = float(parsed.get("overall", 0))

    if overall < threshold:
        scores_display = ""
        if "scores" in parsed:
            scores_display = "\n".join(
                f"  {k}: {v:.2f}" for k, v in parsed["scores"].items()
            )
        raise AssertionError(
            f"Rubric score {overall:.2f} below threshold {threshold:.2f}\n"
            f"Per-criterion scores:\n{scores_display}\n"
            f"Reasoning: {parsed.get('reasoning', 'N/A')}"
        )

    return parsed
