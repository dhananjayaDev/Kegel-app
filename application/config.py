"""Application configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-production")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    DATA_DIR = BASE_DIR / "data"

    # web | desktop | android — controls LLM auto-detection priority
    APP_DEPLOYMENT = os.getenv("APP_DEPLOYMENT", "web").lower()

    # auto | ollama | gemini | template
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    # ── Hosted deployment: set GEMINI_API_KEY to enable cloud LLM ──
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    DESKTOP_APP_URL = os.getenv("DESKTOP_APP_URL", "")
    MOBILE_APP_URL = os.getenv("MOBILE_APP_URL", "")

    DATABASE_URL = os.getenv("DATABASE_URL", "")

    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "5000"))
