"""Google Gemini API client — for hosted deployment."""

from __future__ import annotations

import requests

from application.llm.base import LLMClient
from application.llm.errors import LLMRateLimitError


class GeminiClient(LLMClient):
    """
    Hosted-site LLM provider.

    Set GEMINI_API_KEY in environment to enable.
    """

    def __init__(self, api_key: str, model: str) -> None:
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Set it in your environment for hosted deployment."
            )
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        response = requests.post(
            url,
            json={
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            },
            timeout=120,
        )
        if response.status_code in (429, 503):
            raise LLMRateLimitError(
                f"Gemini rate limit or capacity error (HTTP {response.status_code})"
            )

        if response.status_code >= 400:
            error_text = response.text.lower()
            try:
                payload = response.json()
                error_text = str(payload.get("error", payload)).lower()
            except ValueError:
                pass
            if any(
                token in error_text
                for token in ("quota", "rate limit", "resource_exhausted", "too many requests")
            ):
                raise LLMRateLimitError(
                    f"Gemini quota or rate limit reached (HTTP {response.status_code})"
                )
            response.raise_for_status()

        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        return parts[0].get("text", "").strip() if parts else ""
