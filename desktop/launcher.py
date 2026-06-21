"""Windows desktop launcher — embedded Flask + native window."""

from __future__ import annotations

import os
import socket
import sys
import threading
import time
from pathlib import Path

# Packaged exe: resources live next to the binary
if getattr(sys, "frozen", False):
    ROOT = Path(sys._MEIPASS)
    os.chdir(ROOT)
else:
    ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("APP_DEPLOYMENT", "desktop")
os.environ.setdefault("LLM_PROVIDER", "auto")
os.environ.setdefault("FLASK_DEBUG", "0")
os.environ.setdefault("FLASK_HOST", "127.0.0.1")
os.environ.setdefault("FLASK_PORT", "8765")

HOST = os.environ["FLASK_HOST"]
PORT = int(os.environ["FLASK_PORT"])
APP_URL = f"http://{HOST}:{PORT}"


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.15)
    return False


def _run_flask() -> None:
    from application import create_app

    app = create_app()
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False, threaded=True)


def main() -> None:
    server = threading.Thread(target=_run_flask, daemon=True)
    server.start()

    if not _wait_for_port(HOST, PORT):
        raise RuntimeError(f"Flask server did not start on {APP_URL}")

    import webview

    webview.create_window(
        "Kegel Health",
        APP_URL,
        width=1100,
        height=820,
        min_size=(360, 640),
    )
    webview.start()


if __name__ == "__main__":
    main()
