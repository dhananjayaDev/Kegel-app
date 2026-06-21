"""Generate Windows .ico from application/static/icons/kegel.png."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "application" / "static" / "icons" / "kegel.png"
ICO = Path(__file__).resolve().parent / "assets" / "kegel.ico"


def main() -> None:
    ICO.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(PNG).convert("RGBA")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    image.save(ICO, format="ICO", sizes=sizes)
    print(f"Wrote {ICO}")


if __name__ == "__main__":
    main()
