"""Auto cost tracking — calculate API costs by provider and model.

Pricing is approximate and updated periodically. For exact costs,
always check the provider's pricing page.

Last updated: Feb 2026
"""

from __future__ import annotations

from vigil.core.results import TestResult

# Pricing per million tokens: (input_price, output_price)
PRICING: dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-4": (30.00, 60.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    "o1": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    "o3-mini": (1.10, 4.40),
    # Anthropic
    "claude-opus-4-20250514": (15.00, 75.00),
    "claude-sonnet-4-20250514": (3.00, 15.00),
    "claude-haiku-4-5-20251001": (0.80, 4.00),
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-opus-20240229": (15.00, 75.00),
    # Google
    "gemini-2.0-flash": (0.10, 0.40),
    "gemini-1.5-pro": (1.25, 5.00),
    "gemini-1.5-flash": (0.075, 0.30),
    # Deepseek
    "deepseek-chat": (0.14, 0.28),
    "deepseek-reasoner": (0.55, 2.19),
}

# Aliases for common short names
_ALIASES: dict[str, str] = {
    "gpt4": "gpt-4",
    "gpt4o": "gpt-4o",
    "gpt4o-mini": "gpt-4o-mini",
    "claude-opus": "claude-opus-4-20250514",
    "claude-sonnet": "claude-sonnet-4-20250514",
    "claude-haiku": "claude-haiku-4-5-20251001",
    "opus": "claude-opus-4-20250514",
    "sonnet": "claude-sonnet-4-20250514",
    "haiku": "claude-haiku-4-5-20251001",
}


def _resolve_model(model: str) -> str:
    """Resolve model aliases and partial matches."""
    if model in PRICING:
        return model
    if model in _ALIASES:
        return _ALIASES[model]
    # Try partial match
    for key in PRICING:
        if model in key or key in model:
            return key
    return model


def calculate_cost(
    model: str,
    tokens_input: int,
    tokens_output: int,
) -> float | None:
    """Calculate the cost for a given model and token counts.

    Returns cost in dollars, or None if model is not in the pricing table.
    """
    resolved = _resolve_model(model)
    if resolved not in PRICING:
        return None

    input_price, output_price = PRICING[resolved]
    cost = (tokens_input * input_price + tokens_output * output_price) / 1_000_000
    return cost


def enrich_result(result: TestResult) -> TestResult:
    """Enrich a TestResult with cost data if model and tokens are available.

    Modifies the result in place and returns it.
    """
    if result.cost is not None:
        return result

    if result.model and result.tokens_input is not None and result.tokens_output is not None:
        result.cost = calculate_cost(result.model, result.tokens_input, result.tokens_output)

    return result


def list_models() -> list[str]:
    """List all models with known pricing."""
    return sorted(PRICING.keys())


def get_pricing(model: str) -> tuple[float, float] | None:
    """Get pricing for a model as (input_per_million, output_per_million)."""
    resolved = _resolve_model(model)
    return PRICING.get(resolved)
