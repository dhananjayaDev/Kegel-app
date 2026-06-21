"""Site header component."""

from __future__ import annotations

from application.components.base import UIComponent


class SiteHeader(UIComponent):
    template_name = "components/header.html"

    def __init__(
        self,
        brand: str = "Kegel Health",
        tagline: str = "Anonymous assessment",
        cta_label: str = "How it works",
        cta_url: str = "/about",
    ) -> None:
        self.brand = brand
        self.tagline = tagline
        self.cta_label = cta_label
        self.cta_url = cta_url

    def context(self) -> dict:
        return {
            "brand": self.brand,
            "tagline": self.tagline,
            "cta_label": self.cta_label,
            "cta_url": self.cta_url,
        }
