# Agent Types

Vigil can test any AI agent through three built-in runners.

## FunctionAgent

Wraps any Python function (sync or async).

```python
from vigil import FunctionAgent

# Simple function
def my_agent(message: str) -> str:
    return "Hello!"

agent = FunctionAgent(my_agent)
result = agent.run("Hi")

# Function returning structured data
def smart_agent(message: str) -> dict:
    return {
        "output": "Hello!",
        "cost": 0.001,
        "tokens_input": 10,
        "tokens_output": 20,
        "model": "gpt-4o-mini",
    }

agent = FunctionAgent(smart_agent)

# Async function
async def async_agent(message: str) -> str:
    return await some_api.call(message)

agent = FunctionAgent(async_agent)
result = agent.run("Hi")            # sync
result = await agent.arun("Hi")     # async

# Default kwargs
agent = FunctionAgent(my_agent, temperature=0.0)
```

## HTTPAgent

Tests agents exposed as HTTP endpoints.

```python
from vigil import HTTPAgent

agent = HTTPAgent("http://localhost:8000/chat")
result = agent.run("Hello!")

# Custom keys
agent = HTTPAgent(
    "http://localhost:8000/api",
    input_key="message",
    output_key="response",
    headers={"Authorization": "Bearer token"},
    timeout=30.0,
)

# Async
result = await agent.arun("Hello!")
```

## CLIAgent

Tests agents as command-line tools.

```python
from vigil import CLIAgent

# Input as argument
agent = CLIAgent("python my_agent.py")
result = agent.run("Hello!")  # runs: python my_agent.py 'Hello!'

# Input via stdin
agent = CLIAgent("python my_agent.py", input_mode="stdin")
result = agent.run("Hello!")
```

## Custom Agents

Use the plugin system to create your own:

```python
from vigil.plugins import register_agent
from vigil.core.results import TestResult

@register_agent("websocket")
class WebSocketAgent:
    def __init__(self, url):
        self.url = url

    def run(self, input: str, **kwargs) -> TestResult:
        # Your implementation
        return TestResult(output="response")
```
