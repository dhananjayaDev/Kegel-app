"""Google Gemini API client — for hosted deployment."""

from __future__ import annotations

import requests

from application.llm.base import LLMClient


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
        response.raise_for_status()
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        return parts[0].get("text", "").strip() if parts else ""
