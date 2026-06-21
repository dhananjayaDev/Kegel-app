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
    app.run(host="0.0.0.0", port=5000, debug=debug, use_reloader=debug)
