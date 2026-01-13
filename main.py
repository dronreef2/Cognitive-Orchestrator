from __future__ import annotations

import sys
from pathlib import Path

# Ensure local src package is importable when running `python main.py`
sys.path.append(str(Path(__file__).parent))

from src.agents import Critic, Editor, Researcher
from src.connectors import gemini_client, ollama_client, openai_client
from src.guardrails import verify


def orchestrate(topic: str) -> None:
    researcher = Researcher(connector=gemini_client())
    critic = Critic(connector=ollama_client())
    editor = Editor(connector=openai_client())

    research_notes = researcher.run(topic)
    print("\n=== Research Notes (Gemini) ===\n", research_notes)

    critique = critic.run(topic, research_notes)
    print("\n=== Critique (Ollama) ===\n", critique)

    if not verify("Review the critique above. Approve to continue to editing."):
        print("Execution halted by human reviewer.")
        return

    final_output = editor.run(topic, research_notes, critique)
    print("\n=== Final Draft (OpenAI) ===\n", final_output)


if __name__ == "__main__":
    user_topic = input("Topic to explore: ").strip()
    if not user_topic:
        print("No topic provided. Exiting.")
        sys.exit(0)
    orchestrate(user_topic)
