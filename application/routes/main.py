"""Main site routes."""

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

from application.components.layout import PageLayout
from application.providers.registry import ProviderRegistry
from application.services.quiz_helpers import first_question, flatten_questions
from application.services.research_doc import research_doc_html

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
    return {"first_question": _get_first_question()}


@main_bp.route("/")
def index():
    session.pop(DRAFT_KEY, None)
    sections = _sections()
    steps = flatten_questions(sections)
    fq = _get_first_question()
    ctx = PageLayout.context(
        active_path="/",
        hero_label="Understand your profile today",
        hero_title="Get your personalized wellness plan",
        hero_subtitle="No account required.",
        hero_photos=[
            "images/pexels-lauraoliveira-18795817.jpg",
            "images/pexels-n-voitkevich-4942801.jpg",
            "images/pexels-natalya-velichenko-113472091-10405995.jpg",
            "images/pexels-rebornfilmes-27366102.jpg",
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
        research_html=research_doc_html(),
        first_question=_get_first_question(),
    )
    return render_template("about.html", **ctx)
