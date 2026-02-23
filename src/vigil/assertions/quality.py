"""Quality assertions — hallucination detection, coherence checks."""

from __future__ import annotations

from vigil.core.results import TestResult


def _get_output(result: TestResult | str) -> str:
    if isinstance(result, TestResult):
        return result.output
    return result


def _check_grounding(output: str, context: str, threshold: float) -> tuple[bool, float, list[str]]:
    """Check if output claims are grounded in context using sentence-level overlap.

    Returns (is_grounded, score, ungrounded_sentences).
    """
    output_sentences = [s.strip() for s in output.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    if not output_sentences:
        return True, 1.0, []

    context_lower = context.lower()
    context_words = set(context_lower.split())

    ungrounded = []
    grounded_count = 0

    for sentence in output_sentences:
        sentence_words = set(sentence.lower().split())
        if not sentence_words:
            grounded_count += 1
            continue

        # A sentence is "grounded" if enough of its content words appear in context
        content_words = {w for w in sentence_words if len(w) > 3}
        if not content_words:
            grounded_count += 1
            continue

        overlap = content_words & context_words
        ratio = len(overlap) / len(content_words)

        if ratio >= threshold:
            grounded_count += 1
        else:
            ungrounded.append(sentence)

    score = grounded_count / len(output_sentences) if output_sentences else 1.0
    return len(ungrounded) == 0, score, ungrounded


def assert_no_hallucination(
    result: TestResult | str,
    context: str,
    threshold: float = 0.5,
) -> None:
    """Assert that the output is grounded in the provided context.

    Checks that the agent's claims can be traced back to the source context.
    Uses word-level overlap as a lightweight heuristic.

    Args:
        result: The agent output to check.
        context: The source context the output should be grounded in.
        threshold: Minimum word overlap ratio per sentence (0.0 to 1.0).
    """
    output = _get_output(result)
    is_grounded, score, ungrounded = _check_grounding(output, context, threshold)

    if not is_grounded:
        ungrounded_display = "\n".join(f"  - {s}" for s in ungrounded[:5])
        raise AssertionError(
            f"Potential hallucination detected (grounding score: {score:.2f})\n"
            f"Ungrounded sentences:\n{ungrounded_display}\n"
            f"These sentences could not be traced to the provided context."
        )
