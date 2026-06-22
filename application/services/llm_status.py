"""Runtime LLM availability snapshot for settings UI and API (on demand only)."""

from __future__ import annotations

from typing import Any

from application.llm.detection import find_ollama, ollama_candidate_urls
from application.llm.factory import LLMFactory


def llm_status(config: Any) -> dict[str, Any]:
    deployment = getattr(config, "APP_DEPLOYMENT", "web").lower()
    provider = getattr(config, "LLM_PROVIDER", "auto").lower()
    probe = find_ollama(config)
    chain = LLMFactory.build_chain(config)

    return {
        "deployment": deployment,
        "provider_mode": provider,
        "ollama": {
            "available": probe is not None,
            "base_url": probe.base_url if probe else getattr(config, "OLLAMA_BASE_URL", ""),
            "models": list(probe.models) if probe else [],
            "selected_model": probe.selected_model if probe else getattr(config, "OLLAMA_MODEL", ""),
            "candidate_urls": ollama_candidate_urls(config),
        },
        "gemini_configured": bool(getattr(config, "GEMINI_API_KEY", "")),
        "active_chain": [item.label for item in chain],
        "uses_local_llm": any("ollama" in item.label for item in chain),
    }
