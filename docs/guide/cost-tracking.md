# Cost Tracking

Vigil can automatically calculate API costs based on model and token usage.

## Auto-enrichment

If your agent returns a model name and token counts, Vigil calculates the cost:

```python
from vigil import FunctionAgent, enrich_result

def my_agent(msg: str) -> dict:
    return {
        "output": "Hello!",
        "model": "gpt-4o-mini",
        "tokens_input": 50,
        "tokens_output": 100,
    }

agent = FunctionAgent(my_agent)
result = agent.run("Hi")
enrich_result(result)

print(result.cost)  # Auto-calculated from pricing table
```

## Supported Models

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, o1, o1-mini, o3-mini |
| Anthropic | claude-opus-4, claude-sonnet-4, claude-haiku-4.5, claude-3.5-sonnet, claude-3-opus |
| Google | gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash |
| DeepSeek | deepseek-chat, deepseek-reasoner |

## Query Pricing

```python
from vigil.cost import get_pricing, list_models, calculate_cost

# Get pricing for a model
input_price, output_price = get_pricing("gpt-4o-mini")
# (0.15, 0.60) per million tokens

# Calculate specific cost
cost = calculate_cost("gpt-4o-mini", tokens_input=1000, tokens_output=500)

# List all known models
models = list_models()
```

## Aliases

You can use short names:

```python
calculate_cost("haiku", 1000, 500)      # → claude-haiku-4.5
calculate_cost("sonnet", 1000, 500)     # → claude-sonnet-4
calculate_cost("gpt4o", 1000, 500)      # → gpt-4o
```
