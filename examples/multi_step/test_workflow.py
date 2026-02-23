"""Example — testing a multi-step agent workflow."""

from vigil import test, FunctionAgent, assert_contains


# Simulated stateful agent
class StatefulAgent:
    def __init__(self):
        self.memory = []

    def chat(self, message: str) -> str:
        self.memory.append(message)

        if "remember" in message.lower() and "name" in message.lower():
            # Extract name
            for word in message.split():
                if word[0].isupper() and word.lower() not in ("remember", "my", "name", "is", "i'm"):
                    self.memory.append(f"USER_NAME={word}")
                    return f"Got it! I'll remember that your name is {word}."
            return "I'll remember that."

        if "what" in message.lower() and "name" in message.lower():
            for item in self.memory:
                if item.startswith("USER_NAME="):
                    name = item.split("=")[1]
                    return f"Your name is {name}!"
            return "I don't know your name yet."

        if "summarize" in message.lower():
            return f"In our conversation, we've exchanged {len(self.memory)} messages."

        return f"Understood: {message}"


stateful = StatefulAgent()
agent = FunctionAgent(stateful.chat)


@test(steps=True)
def test_memory_workflow():
    """Test that the agent remembers information across steps."""
    r1 = agent.run("Remember my name is Alice")
    assert_contains(r1, "Alice")

    r2 = agent.run("What is my name?")
    assert_contains(r2, "Alice")


@test(steps=True)
def test_conversation_flow():
    """Test a multi-turn conversation."""
    r1 = agent.run("Hello there")
    assert_contains(r1, "Understood")

    r2 = agent.run("Please summarize our conversation")
    assert_contains(r2, "messages")
