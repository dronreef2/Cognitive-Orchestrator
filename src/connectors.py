"""Connector abstractions for multiple providers using LiteLLM."""

from __future__ import annotations

from typing import Any, Dict

from litellm import completion


class LLMConnector:
    """Thin wrapper around litellm.completion to normalize chat calls."""

    def __init__(self, model: str) -> None:
        self.model = model

    def chat(self, prompt: str, **kwargs: Any) -> str:
        """Send a user prompt to the configured model and return the text reply."""
        if not prompt:
            raise ValueError("Prompt must be a non-empty string.")
        response: Dict[str, Any] = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Unexpected response format from LiteLLM") from exc
        if content is None:
            raise RuntimeError("LiteLLM response did not include message content")
        return content


def openai_client(model: str = "gpt-4o-mini") -> LLMConnector:
    return LLMConnector(model=model)


def gemini_client(model: str = "gemini/gemini-1.5-flash") -> LLMConnector:
    return LLMConnector(model=model)


def ollama_client(model: str = "ollama/llama3") -> LLMConnector:
    return LLMConnector(model=model)
