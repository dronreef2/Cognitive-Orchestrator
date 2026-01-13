"""Connector abstractions for multiple providers using LiteLLM."""

from __future__ import annotations

from typing import Any, Dict

from litellm import completion

ALLOWED_COMPLETION_KWARGS = {
    "temperature",
    "max_tokens",
    "top_p",
    "presence_penalty",
    "frequency_penalty",
    "stop",
}


class LLMConnector:
    """Thin wrapper around litellm.completion to normalize chat calls."""

    def __init__(self, model: str) -> None:
        self.model = model

    def chat(self, prompt: str, **kwargs: Any) -> str:
        """Send a user prompt to the configured model and return the text reply."""
        if not prompt or not str(prompt).strip():
            raise ValueError("Prompt must be a non-empty string.")
        unexpected = set(kwargs) - ALLOWED_COMPLETION_KWARGS
        if unexpected:
            raise ValueError(f"Unsupported parameters for LiteLLM call: {unexpected}")
        response: Dict[str, Any] = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        if not isinstance(response, dict) or not response.get("choices"):
            raise RuntimeError(f"LiteLLM response missing choices: {response!r}")
        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"Unexpected LiteLLM response structure: {response!r}"
            ) from exc
        if content is None:
            raise RuntimeError(
                f"LiteLLM response returned None content: {response!r}"
            )
        return content


def openai_client(model: str = "gpt-4o-mini") -> LLMConnector:
    return LLMConnector(model=model)


def gemini_client(model: str = "gemini/gemini-1.5-flash") -> LLMConnector:
    return LLMConnector(model=model)


def ollama_client(model: str = "ollama/llama3") -> LLMConnector:
    return LLMConnector(model=model)
