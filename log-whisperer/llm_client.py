"""Unified LLM client supporting multiple providers."""

import os
from typing import List, Dict, Any
from enum import Enum
import config


class LLMProvider(Enum):
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class LLMClient:
    """Unified interface for different LLM providers."""
    
    def __init__(self, provider: str = None):
        """Initialize LLM client with specified provider."""
        if provider is None:
            provider = config.LLM_PROVIDER
        
        self.provider = LLMProvider(provider.lower())
        self.client = None
        
        if self.provider == LLMProvider.ANTHROPIC:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        elif self.provider == LLMProvider.GEMINI:
            from google import genai
            from google.genai import types
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    def create_message(
        self,
        model: str,
        max_tokens: int,
        system: str,
        messages: List[Dict[str, str]],
        temperature: float = 1.0
    ) -> str:
        """Create a message using the configured provider."""
        
        if self.provider == LLMProvider.ANTHROPIC:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
                temperature=temperature
            )
            return response.content[0].text
        
        elif self.provider == LLMProvider.GEMINI:
            # Map Anthropic model names to Gemini equivalents
            # Using Flash models for better rate limits on free tier
            model_map = {
                "claude-sonnet-4-20250514": "models/gemini-2.5-flash",
                "claude-3-5-sonnet-20241022": "models/gemini-2.0-flash",
                "claude-3-sonnet-20240229": "models/gemini-2.5-flash",
            }
            gemini_model = model_map.get(model, "models/gemini-2.5-flash")
            
            # Combine system prompt with user message for Gemini
            user_content = messages[0]["content"]
            full_prompt = f"{system}\n\n{user_content}"
            
            response = self.client.models.generate_content(
                model=gemini_model,
                contents=full_prompt,
                config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature,
                }
            )
            
            # Handle response
            if hasattr(response, 'text') and response.text:
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                raise ValueError(f"Unexpected Gemini response format: {response}")
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")


def get_llm_client() -> LLMClient:
    """Get configured LLM client instance."""
    return LLMClient()
