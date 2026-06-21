"""LLM client factory."""

from __future__ import annotations

from typing import Any

from application.llm.base import LLMClient
from application.llm.gemini import GeminiClient
from application.llm.ollama import OllamaClient


class LLMFactory:
    @staticmethod
    def create(config: Any) -> LLMClient | None:
        provider = getattr(config, "LLM_PROVIDER", "ollama").lower()

        if provider == "gemini":
            api_key = getattr(config, "GEMINI_API_KEY", "")
            if api_key:
                return GeminiClient(api_key, getattr(config, "GEMINI_MODEL", "gemini-2.0-flash"))
            return None

        if provider == "template":
            return None

        return OllamaClient(
            getattr(config, "OLLAMA_BASE_URL", "http://localhost:11434"),
            getattr(config, "OLLAMA_MODEL", "llama3.2"),
        )
