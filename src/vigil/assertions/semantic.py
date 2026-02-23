"""Semantic similarity assertions."""

from __future__ import annotations

from vigil.core.results import TestResult


def _get_output(result: TestResult | str) -> str:
    if isinstance(result, TestResult):
        return result.output
    return result


def _word_overlap_similarity(text1: str, text2: str) -> float:
    """Simple word overlap similarity (Jaccard index). No external deps needed."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


def _cosine_similarity_numpy(text1: str, text2: str) -> float:
    """Cosine similarity using TF-IDF-like vectors with numpy."""
    try:
        import numpy as np
    except ImportError:
        return _word_overlap_similarity(text1, text2)

    words1 = text1.lower().split()
    words2 = text2.lower().split()
    all_words = list(set(words1 + words2))

    vec1 = np.array([words1.count(w) for w in all_words], dtype=float)
    vec2 = np.array([words2.count(w) for w in all_words], dtype=float)

    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot / (norm1 * norm2))


def assert_semantic_match(
    result: TestResult | str,
    reference: str,
    threshold: float = 0.7,
    method: str = "auto",
) -> None:
    """Assert that the output is semantically similar to the reference text.

    Args:
        result: The agent output to check.
        reference: The reference text to compare against.
        threshold: Minimum similarity score (0.0 to 1.0).
        method: Similarity method — "auto", "word_overlap", or "cosine".
    """
    output = _get_output(result)

    if method == "auto":
        try:
            import numpy  # noqa: F401

            score = _cosine_similarity_numpy(output, reference)
        except ImportError:
            score = _word_overlap_similarity(output, reference)
    elif method == "word_overlap":
        score = _word_overlap_similarity(output, reference)
    elif method == "cosine":
        score = _cosine_similarity_numpy(output, reference)
    else:
        raise ValueError(f"Unknown method: {method}. Use 'auto', 'word_overlap', or 'cosine'.")

    if score < threshold:
        raise AssertionError(
            f"Semantic similarity {score:.3f} below threshold {threshold:.3f}\n"
            f"Output: '{output[:100]}{'...' if len(output) > 100 else ''}'\n"
            f"Reference: '{reference[:100]}{'...' if len(reference) > 100 else ''}'"
        )
