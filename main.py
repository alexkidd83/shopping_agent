"""
Entry point for the shopping agent package. This module defines a
placeholder LLM class and demonstrates how you might wire it up with a
system prompt and orchestrator. For actual use, run the `ui.py` module
instead (e.g. python3 -m shopping_agent.ui run).
"""

from __future__ import annotations

from .memory import Memory
from .orchestrator import Orchestrator


class LLM:
    """
    Placeholder language model class. Replace the `call` method with
    integration code for a real LLM API or local model. This class
    accepts a prompt and returns a dummy completion.
    """

    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt

    def call(self, user_message: str) -> str:
        # In a real implementation you would combine the system prompt and
        # user message, send them to the model and return the response.
        return f"[LLM Stub] You said: {user_message}"


def load_system_prompt() -> str:
    import pkg_resources
    prompt_path = pkg_resources.resource_filename(
        "shopping_agent", "prompts/system_prompt.txt"
    )
    with open(prompt_path, "r") as f:
        return f.read().strip()


def run_agent() -> None:
    system_prompt = load_system_prompt()
    llm = LLM(system_prompt)
    mem = Memory()
    orchestrator = Orchestrator(mem)
    # Example usage of the LLM stub
    response = llm.call("What should I do today?")
    print(response)
    orchestrator.run()


if __name__ == "__main__":
    run_agent()
