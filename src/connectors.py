"""
Multi-provider LLM connector setup using litellm.
Supports OpenAI and Gemini providers.
"""

import os
from typing import Optional, Dict, Any
from litellm import completion


class LLMConnector:
    """
    A unified interface for multiple LLM providers using litellm.
    Supports OpenAI and Gemini models.
    """
    
    def __init__(self, provider: str = "openai", model: Optional[str] = None):
        """
        Initialize the LLM connector.
        
        Args:
            provider: The LLM provider to use ("openai" or "gemini")
            model: The specific model to use (defaults based on provider)
        """
        self.provider = provider.lower()
        
        # Set default models based on provider
        if model is None:
            if self.provider == "openai":
                self.model = "gpt-4"
            elif self.provider == "gemini":
                self.model = "gemini/gemini-pro"
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        else:
            self.model = model
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt/message
            system_prompt: Optional system message to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            **kwargs: Additional arguments to pass to litellm
            
        Returns:
            The generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise RuntimeError(f"Error generating response from {self.provider}: {str(e)}")
    
    def __repr__(self) -> str:
        return f"LLMConnector(provider='{self.provider}', model='{self.model}')"


def get_connector(provider: str = "openai", model: Optional[str] = None) -> LLMConnector:
    """
    Factory function to get an LLM connector.
    
    Args:
        provider: The LLM provider to use
        model: The specific model to use
        
    Returns:
        An initialized LLMConnector instance
    """
    return LLMConnector(provider=provider, model=model)
