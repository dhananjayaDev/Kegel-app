"""LLM client factory with auto-detection and fallback chains."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from application.llm.base import LLMClient
from application.llm.detection import find_ollama
from application.llm.gemini import GeminiClient
from application.llm.ollama import OllamaClient


@dataclass(frozen=True)
class ResolvedLLM:
    client: LLMClient
    label: str


class LLMFactory:
    @staticmethod
    def create(config: Any) -> LLMClient | None:
        resolved = LLMFactory.resolve_primary(config)
        return resolved.client if resolved else None

    @staticmethod
    def resolve_primary(config: Any) -> ResolvedLLM | None:
        chain = LLMFactory.build_chain(config)
        return chain[0] if chain else None

    @staticmethod
    def build_chain(config: Any) -> list[ResolvedLLM]:
        provider = getattr(config, "LLM_PROVIDER", "auto").lower()
        deployment = getattr(config, "APP_DEPLOYMENT", "web").lower()

        if provider == "template":
            return []

        if provider == "gemini":
            client = LLMFactory._gemini_client(config)
            return [ResolvedLLM(client, "gemini")] if client else []

        if provider == "ollama":
            resolved = LLMFactory._ollama_client(config)
            return [ResolvedLLM(resolved, "ollama")] if resolved else []

        # auto — deployment-specific priority
        chain: list[ResolvedLLM] = []

        if deployment in ("desktop", "android"):
            ollama = LLMFactory._ollama_client(config)
            if ollama:
                chain.append(ResolvedLLM(ollama, "ollama (local)"))
            gemini = LLMFactory._gemini_client(config)
            if gemini:
                chain.append(ResolvedLLM(gemini, "gemini"))
            return chain

        # web: cloud first, optional local Ollama for dev
        gemini = LLMFactory._gemini_client(config)
        if gemini:
            chain.append(ResolvedLLM(gemini, "gemini"))
        ollama = LLMFactory._ollama_client(config)
        if ollama:
            chain.append(ResolvedLLM(ollama, "ollama (local)"))
        return chain

    @staticmethod
    def _gemini_client(config: Any) -> GeminiClient | None:
        api_key = getattr(config, "GEMINI_API_KEY", "")
        if not api_key:
            return None
        return GeminiClient(api_key, getattr(config, "GEMINI_MODEL", "gemini-2.0-flash"))

    @staticmethod
    def _ollama_client(config: Any) -> OllamaClient | None:
        probe = find_ollama(config)
        if not probe:
            return None
        return OllamaClient(probe.base_url, probe.selected_model)
