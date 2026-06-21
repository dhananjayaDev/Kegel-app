"""Start embedded Flask for the Android WebView shell."""

from __future__ import annotations

import os
import threading

os.environ.setdefault("APP_DEPLOYMENT", "android")
os.environ.setdefault("LLM_PROVIDER", "auto")
os.environ.setdefault("FLASK_DEBUG", "0")
os.environ.setdefault("FLASK_HOST", "127.0.0.1")
os.environ.setdefault("FLASK_PORT", "5000")

_started = False


def start_server() -> None:
    global _started
    if _started:
        return
    _started = True

    def _run() -> None:
        from application import create_app

        app = create_app()
        app.run(
            host=os.environ["FLASK_HOST"],
            port=int(os.environ["FLASK_PORT"]),
            debug=False,
            use_reloader=False,
            threaded=True,
        )

    threading.Thread(target=_run, daemon=True).start()
