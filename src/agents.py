"""Agent definitions for the orchestration pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from .connectors import LLMConnector


@dataclass
class Researcher:
    connector: LLMConnector

    def run(self, topic: str) -> str:
        prompt = (
            "You are a research agent. Gather concise context, facts, and sources "
            f"to explain: {topic}. Keep it factual and bullet-like."
        )
        return self.connector.chat(prompt)


@dataclass
class Critic:
    connector: LLMConnector

    def run(self, topic: str, research_notes: str) -> str:
        prompt = (
            "You are a critical analyst. Review the research notes for logical gaps, "
            "missing perspectives, and risks. Respond with a numbered list of critiques "
            f"for the topic '{topic}'.\n\nResearch Notes:\n{research_notes}"
        )
        return self.connector.chat(prompt)


@dataclass
class Editor:
    connector: LLMConnector

    def run(self, topic: str, research_notes: str, critique: str) -> str:
        prompt = (
            "You are an editor focused on clarity and style. Produce a polished, "
            "reader-friendly summary that incorporates research and addresses critiques. "
            f"Topic: {topic}\n\nResearch Notes:\n{research_notes}\n\nCritique:\n{critique}"
        )
        return self.connector.chat(prompt)
