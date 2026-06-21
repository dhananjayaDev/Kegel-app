"""Application entry point.

Run locally:
    python app.py

Deploy (e.g. gunicorn):
    gunicorn app:app
"""

from application import create_app

app = create_app()

if __name__ == "__main__":
    debug = app.config.get("DEBUG", False)
    host = app.config.get("HOST", "0.0.0.0")
    port = app.config.get("PORT", 5000)
    app.run(host=host, port=port, debug=debug, use_reloader=debug)
