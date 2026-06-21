"""Base provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """Base class for modular context providers."""

    name: str = "base"

    @abstractmethod
    def invoke(self, payload: dict[str, Any]) -> Any:
        """Execute provider logic with a structured payload."""
