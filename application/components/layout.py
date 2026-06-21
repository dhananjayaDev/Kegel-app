"""Page layout composer — single source for header/footer."""

from __future__ import annotations

from application.components.footer import SiteFooter
from application.components.header import SiteHeader


class PageLayout:
    """Composes reusable chrome; pages must not duplicate header/footer markup."""

    _header = SiteHeader()
    _footer = SiteFooter()

    @classmethod
    def context(cls, **extra) -> dict:
        return {
            "header": cls._header.context(),
            "footer": cls._footer.context(),
            **extra,
        }
