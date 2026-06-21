"""OOP UI component base."""

from __future__ import annotations

from abc import ABC, abstractmethod


class UIComponent(ABC):
    template_name: str = ""

    @abstractmethod
    def context(self) -> dict:
        """Return template context for this component."""

    def render_context(self) -> dict:
        return {self.__class__.__name__.lower(): self.context()}
