# Plugins

Extend Vigil with custom assertions, agents, and reporters.

## Custom Assertions

```python
from vigil.plugins import register_assertion
from vigil.core.results import TestResult

@register_assertion("assert_polite")
def assert_polite(result, **kwargs):
    output = result.output if isinstance(result, TestResult) else str(result)
    polite_words = ["please", "thank", "sorry", "appreciate"]
    if not any(word in output.lower() for word in polite_words):
        raise AssertionError("Output is not polite")
```

Use it:

```python
from vigil.plugins import get_assertion

assert_polite = get_assertion("assert_polite")
assert_polite(result)
```

## Custom Agents

```python
from vigil.plugins import register_agent
from vigil.core.results import TestResult

@register_agent("grpc")
class GRPCAgent:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def run(self, input: str, **kwargs) -> TestResult:
        # Your gRPC logic
        return TestResult(output="response")
```

## Custom Reporters

```python
from vigil.plugins import register_reporter

@register_reporter("slack")
class SlackReporter:
    def __init__(self):
        self.results = []

    def add_result(self, name, passed, **kwargs):
        self.results.append({"name": name, "passed": passed})

    def render(self):
        # Send to Slack
        pass
```

## Entry Points (for packages)

If you're publishing a Vigil plugin as a package, register via entry points:

```toml
# In your plugin's pyproject.toml
[project.entry-points."vigil.assertions"]
assert_polite = "my_plugin:assert_polite"

[project.entry-points."vigil.agents"]
grpc = "my_plugin:GRPCAgent"

[project.entry-points."vigil.reporters"]
slack = "my_plugin:SlackReporter"
```

Vigil auto-discovers entry points at startup.
