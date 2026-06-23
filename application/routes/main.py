"""Main site routes."""

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, send_file, session, url_for

from application.components.layout import PageLayout
from application.providers.registry import ProviderRegistry
from application.config import Config
from application.services.download_links import find_desktop_installer
from application.services.quiz_helpers import first_question, flatten_questions
from application.services.research_doc import research_doc_html
from application.services.llm_status import llm_status
from application.services.site_stats import get_stats, increment_stat

main_bp = Blueprint("main", __name__)
DRAFT_KEY = "quiz_draft"


def _sections():
    registry: ProviderRegistry = current_app.extensions["providers"]
    return registry.invoke("questionnaire", {"action": "sections"})


def _default_first_question():
    return {
        "id": "age_group",
        "text": "What is your age group?",
        "options": [
            {"value": "under_30", "label": "Under 30"},
            {"value": "30_39", "label": "30–39"},
            {"value": "40_49", "label": "40–49"},
            {"value": "50_59", "label": "50–59"},
            {"value": "60_plus", "label": "60 and over"},
        ],
    }


def _get_first_question():
    fq = first_question(_sections())
    return fq or _default_first_question()


@main_bp.context_processor
def _inject_quiz_context():
    return {
        "first_question": _get_first_question(),
    }


@main_bp.route("/")
def index():
    session.pop(DRAFT_KEY, None)
    sections = _sections()
    steps = flatten_questions(sections)
    fq = _get_first_question()
    db_url = current_app.config.get("DATABASE_URL", "")
    site_stats = increment_stat(db_url, "site_visits") or get_stats(db_url) or {
        "site_visits": 0,
        "downloads": 0,
        "quizzes": 0,
    }
    ctx = PageLayout.context(
        active_path="/",
        hero_label="Understand your profile today",
        hero_title="Get your personalized wellness plan",
        hero_subtitle="No account required.",
        site_stats=site_stats,
        hero_photos=[
            "images/pexels-lauraoliveira-18795817.webp",
            "images/pexels-n-voitkevich-4942801.webp",
            "images/pexels-natalya-velichenko-113472091-10405995.webp",
            "images/pexels-rebornfilmes-27366102.webp",
        ],
        first_question=fq,
        total_steps=len(steps) or 34,
    )
    return render_template("index.html", **ctx)


@main_bp.route("/start", methods=["POST"])
def start_assessment():
    """Save age from home page and continue to question 2."""
    age_group = request.form.get("age_group")
    if not age_group:
        return redirect(url_for("main.index"))

    session[DRAFT_KEY] = {"age_group": age_group}
    return redirect(url_for("questionnaire.start"))


@main_bp.route("/about")
def about():
    ctx = PageLayout.context(
        active_path="/about",
        research_html=research_doc_html(current_app.config["BASE_DIR"]),
        first_question=_get_first_question(),
    )
    return render_template("about.html", **ctx)


@main_bp.route("/terms")
def terms():
    ctx = PageLayout.context(active_path="/terms")
    return render_template("terms.html", **ctx)


@main_bp.route("/privacy")
def privacy():
    ctx = PageLayout.context(active_path="/privacy")
    return render_template("privacy.html", **ctx)


@main_bp.route("/download/desktop")
def download_desktop():
    db_url = current_app.config.get("DATABASE_URL", "")
    external_url = (current_app.config.get("DESKTOP_APP_URL", "") or "").strip()
    if external_url:
        increment_stat(db_url, "downloads")
        return redirect(external_url)

    installer = find_desktop_installer(Config.BASE_DIR)
    if not installer:
        return redirect(url_for("main.index"))
    increment_stat(db_url, "downloads")
    return send_file(
        installer,
        as_attachment=True,
        download_name=installer.name,
    )


@main_bp.route("/api/llm/status")
def llm_status_api():
    return jsonify(llm_status(current_app.config))


@main_bp.route("/settings", methods=["GET", "POST"])
def settings():
    deployment = current_app.config.get("APP_DEPLOYMENT", "web")
    if deployment not in ("desktop", "android"):
        return redirect(url_for("main.index"))

    saved = False
    if request.method == "POST":
        base_url = (request.form.get("ollama_base_url") or "").strip()
        model = (request.form.get("ollama_model") or "").strip()
        if base_url:
            session["ollama_base_url"] = base_url
        if model:
            session["ollama_model"] = model
        saved = True

    ctx = PageLayout.context(
        active_path="/settings",
        ollama_base_url=session.get("ollama_base_url", current_app.config.get("OLLAMA_BASE_URL", "")),
        ollama_model=session.get("ollama_model", current_app.config.get("OLLAMA_MODEL", "")),
        settings_saved=saved,
        llm_status=llm_status(current_app.config),
    )
    return render_template("settings.html", **ctx)
