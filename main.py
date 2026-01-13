from __future__ import annotations

import os
import sys

from src.agents import Critic, Editor, Researcher
from src.connectors import LLMConnector, gemini_client, ollama_client, openai_client
from src.guardrails import verify


def _connector_for_model(model_name: str) -> LLMConnector:
    normalized = (model_name or "").lower()
    if normalized.startswith("gemini"):
        return gemini_client(model_name)
    if normalized.startswith("ollama"):
        return ollama_client(model_name)
    return openai_client(model_name)


def orchestrate(topic: str) -> None:
    researcher_model = os.getenv("RESEARCH_MODEL", "gemini/gemini-1.5-flash")
    critic_model = os.getenv("CRITIC_MODEL", "ollama/llama3")
    editor_model = os.getenv("EDITOR_MODEL", "gpt-4o-mini")

    researcher = Researcher(connector=_connector_for_model(researcher_model))
    critic = Critic(connector=_connector_for_model(critic_model))
    editor = Editor(connector=_connector_for_model(editor_model))

    research_notes = researcher.run(topic)
    print(f"\n=== Research Notes ({researcher_model}) ===\n", research_notes)

    critique = critic.run(topic, research_notes)
    print(f"\n=== Critique ({critic_model}) ===\n", critique)

    if not verify("Review the critique above. Approve to continue to editing."):
        print("Execution halted by human reviewer.")
        return

    final_output = editor.run(topic, research_notes, critique)
    print(f"\n=== Final Draft ({editor_model}) ===\n", final_output)


if __name__ == "__main__":
    try:
        user_topic = input("Topic to explore: ").strip()
    except EOFError:
        print("No interactive input available. Exiting.")
        sys.exit(0)
    if not user_topic:
        print("No topic provided. Exiting.")
        sys.exit(0)
    orchestrate(user_topic)
