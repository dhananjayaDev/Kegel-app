"""LLM client errors."""


class LLMError(Exception):
    """Base error for LLM provider failures."""


class LLMRateLimitError(LLMError):
    """Raised when the provider rejects requests due to quota or rate limits."""
