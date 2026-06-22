"""Probe local Ollama and pick an available model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


def _session_override(key: str) -> str | None:
    try:
        from flask import has_request_context, session

        if has_request_context():
            value = session.get(key)
            if value:
                return str(value).strip()
    except ImportError:
        pass
    return None


@dataclass(frozen=True)
class OllamaProbeResult:
    available: bool
    base_url: str
    models: tuple[str, ...]
    selected_model: str


def _normalize_model_name(name: str) -> str:
    return name.split(":")[0] if ":" in name else name


def _model_matches(configured: str, available_name: str) -> bool:
    configured_base = _normalize_model_name(configured).lower()
    available_base = _normalize_model_name(available_name).lower()
    return configured_base == available_base or configured_base in available_name.lower()


def pick_ollama_model(configured: str, models: list[str]) -> str:
    if not models:
        return configured

    for name in models:
        if _model_matches(configured, name):
            return name

    preferred = ("llama3.2", "llama3", "llama", "mistral", "phi", "gemma")
    for token in preferred:
        for name in models:
            if token in name.lower():
                return name

    return models[0]


def probe_ollama(base_url: str, configured_model: str, timeout: float = 3.0) -> OllamaProbeResult:
    url = base_url.rstrip("/")
    try:
        response = requests.get(f"{url}/api/tags", timeout=timeout)
        response.raise_for_status()
        models = [item.get("name", "") for item in response.json().get("models", []) if item.get("name")]
        selected = pick_ollama_model(configured_model, models)
        return OllamaProbeResult(
            available=bool(models),
            base_url=url,
            models=tuple(models),
            selected_model=selected,
        )
    except (requests.RequestException, ValueError):
        return OllamaProbeResult(
            available=False,
            base_url=url,
            models=(),
            selected_model=configured_model,
        )


def ollama_candidate_urls(config: Any) -> list[str]:
    """Build ordered list of Ollama URLs to try for this deployment."""
    urls: list[str] = []
    primary = _session_override("ollama_base_url") or getattr(
        config, "OLLAMA_BASE_URL", "http://localhost:11434"
    )
    primary = primary.rstrip("/")
    deployment = getattr(config, "APP_DEPLOYMENT", "web").lower()

    for candidate in (primary, "http://127.0.0.1:11434", "http://localhost:11434"):
        if candidate not in urls:
            urls.append(candidate)

    if deployment == "android":
        for candidate in ("http://10.0.2.2:11434",):
            if candidate not in urls:
                urls.append(candidate)

    return urls


def find_ollama(config: Any) -> OllamaProbeResult | None:
    try:
        from flask import g, has_request_context

        if has_request_context() and hasattr(g, "_ollama_probe"):
            return g._ollama_probe
    except ImportError:
        pass

    configured_model = _session_override("ollama_model") or getattr(config, "OLLAMA_MODEL", "llama3.2")
    result: OllamaProbeResult | None = None
    for base_url in ollama_candidate_urls(config):
        probe = probe_ollama(base_url, configured_model)
        if probe.available:
            result = probe
            break

    try:
        from flask import g, has_request_context

        if has_request_context():
            g._ollama_probe = result
    except ImportError:
        pass

    return result
