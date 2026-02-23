"""Basic example — testing a simple agent with no API keys needed."""

from vigil import test, FunctionAgent, assert_contains, assert_not_contains


# A mock agent — replace this with your real agent
def my_agent(message: str) -> str:
    """A simple echo agent for demonstration."""
    if "hello" in message.lower():
        return "Hello! I'm an AI assistant. How can I help you today?"
    if "python" in message.lower():
        return "Python is a high-level programming language known for its simplicity and readability."
    return f"You said: {message}"


agent = FunctionAgent(my_agent)


@test()
def test_greeting():
    result = agent.run("Hello!")
    assert_contains(result, "Hello")
    assert_contains(result, "assistant", case_sensitive=False)


@test()
def test_knowledge():
    result = agent.run("Tell me about Python")
    assert_contains(result, "programming language")


@test()
def test_no_harmful_content():
    result = agent.run("Hello!")
    assert_not_contains(result, "error")
    assert_not_contains(result, "exception")


@test(tags=["echo"])
def test_echo_fallback():
    result = agent.run("random input here")
    assert_contains(result, "random input here")
