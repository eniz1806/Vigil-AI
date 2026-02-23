"""Agent runners — wrappers to test any kind of AI agent."""

from vigil.agents.base import AgentUnderTest
from vigil.agents.function import FunctionAgent
from vigil.agents.http import HTTPAgent
from vigil.agents.cli import CLIAgent

__all__ = ["AgentUnderTest", "FunctionAgent", "HTTPAgent", "CLIAgent"]
