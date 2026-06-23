"""Resolve app download URLs for templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import url_for

from application.config import Config


def _desktop_candidates(base_dir: Path) -> list[Path]:
    return [
        base_dir / "dist" / "installer" / "KegelHealth-Setup.exe",
        base_dir / "dist" / "KegelHealth-Setup.exe",
        base_dir / "dist" / "KegelHealth.exe",
        base_dir / "application" / "static" / "downloads" / "KegelHealth-Setup.exe",
        base_dir / "application" / "static" / "downloads" / "KegelHealth.exe",
    ]


def find_desktop_installer(base_dir: Path) -> Path | None:
    for path in _desktop_candidates(base_dir):
        if path.is_file():
            return path
    return None


def _config_str(config: Any, key: str) -> str:
    if hasattr(config, "get"):
        return (config.get(key, "") or "").strip()
    return (getattr(config, key, "") or "").strip()


def resolve_download_links(config: Any) -> dict[str, str | bool]:
    configured_desktop = _config_str(config, "DESKTOP_APP_URL")
    configured_mobile = _config_str(config, "MOBILE_APP_URL")
    base_dir = config.get("BASE_DIR", Config.BASE_DIR) if hasattr(config, "get") else Config.BASE_DIR

    desktop_available = bool(configured_desktop) or find_desktop_installer(base_dir) is not None
    desktop_url = url_for("main.download_desktop") if desktop_available else ""

    mobile_available = bool(configured_mobile)

    return {
        "desktop_app_url": desktop_url,
        "mobile_app_url": configured_mobile,
        "desktop_download_available": desktop_available,
        "mobile_download_available": mobile_available,
        "mobile_download_message": "Mobile app — coming soon",
    }
