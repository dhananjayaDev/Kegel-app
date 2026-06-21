"""Site footer component."""

from __future__ import annotations

from application.components.base import UIComponent


class SiteFooter(UIComponent):
    template_name = "components/footer.html"

    def __init__(self, year: int = 2026) -> None:
        self.year = year

    def context(self) -> dict:
        return {
            "year": self.year,
            "disclaimer": (
                "This tool is for informational purposes only and does not "
                "constitute medical advice, diagnosis, or treatment."
            ),
        }
