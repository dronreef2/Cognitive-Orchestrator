"""Agent definitions for the orchestration pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from .connectors import LLMConnector


def _sanitize_block(text: str) -> str:
    cleaned = (text or "").strip()
    if not cleaned:
        return "[no content]"
    return f"```\n{cleaned}\n```"


@dataclass
class Researcher:
    connector: LLMConnector

    def run(self, topic: str) -> str:
        topic_clean = (topic or "").strip()
        if not topic_clean:
            raise ValueError("Topic must be provided.")
        prompt = (
            "You are a research agent. Gather concise context, facts, and sources "
            "to explain the topic below. Keep it factual and bullet-like.\n\n"
            f"Topic:\n{_sanitize_block(topic_clean)}"
        )
        return self.connector.chat(prompt)


@dataclass
class Critic:
    connector: LLMConnector

    def run(self, topic: str, research_notes: str) -> str:
        topic_clean = (topic or "").strip()
        if not topic_clean:
            raise ValueError("Topic must be provided.")
        prompt = (
            "You are a critical analyst. Review the research notes for logical gaps, "
            "missing perspectives, and risks. Respond with a numbered list of critiques "
            f"for the topic.\n\nTopic:\n{_sanitize_block(topic_clean)}\n\n"
            f"Research Notes:\n{_sanitize_block(research_notes)}"
        )
        return self.connector.chat(prompt)


@dataclass
class Editor:
    connector: LLMConnector

    def run(self, topic: str, research_notes: str, critique: str) -> str:
        topic_clean = (topic or "").strip()
        if not topic_clean:
            raise ValueError("Topic must be provided.")
        prompt = (
            "You are an editor focused on clarity and style. Produce a polished, "
            "reader-friendly summary that incorporates research and addresses critiques. "
            f"\nTopic:\n{_sanitize_block(topic_clean)}\n\n"
            f"Research Notes:\n{_sanitize_block(research_notes)}\n\n"
            f"Critique:\n{_sanitize_block(critique)}"
        )
        return self.connector.chat(prompt)
