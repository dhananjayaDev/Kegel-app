"""Questionnaire and results routes."""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

from application.components.layout import PageLayout
from application.services.assessment_service import AssessmentService
from application.services.quiz_helpers import flatten_questions, options_side_by_side
from application.utils.markdown import render_markdown

questionnaire_bp = Blueprint("questionnaire", __name__)


@questionnaire_bp.app_template_filter("options_side_by_side")
def _options_side_by_side_filter(options: list) -> bool:
    return options_side_by_side(options)

DRAFT_KEY = "quiz_draft"
MULTI_SELECT_IDS = {"q22"}


def _service() -> AssessmentService:
    registry = current_app.extensions["providers"]
    return AssessmentService(registry)


def _draft() -> dict:
    return session.get(DRAFT_KEY, {})


def _quiz_context(sections: list, **extra) -> dict:
    all_steps = flatten_questions(sections)
    draft = _draft()
    skip = 1 if draft.get("age_group") else 0
    steps = all_steps[skip:]
    return {
        **PageLayout.context(active_path="/assessment/"),
        "sections": sections,
        "steps": steps,
        "total_steps": len(all_steps),
        "progress_offset": skip,
        "draft": draft,
        **extra,
    }


@questionnaire_bp.route("/begin", methods=["POST"])
def begin():
    age_group = request.form.get("age_group")
    if not age_group:
        return redirect(url_for("main.index"))

    draft = session.get(DRAFT_KEY, {})
    draft["age_group"] = age_group
    session[DRAFT_KEY] = draft
    return redirect(url_for("questionnaire.start"))


@questionnaire_bp.route("/")
def start():
    draft = _draft()
    if not draft.get("age_group"):
        return redirect(url_for("main.index"))

    sections = _service().get_sections()
    return render_template("questionnaire.html", **_quiz_context(sections))


@questionnaire_bp.route("/submit", methods=["POST"])
def submit():
    form = request.form
    draft = _draft()

    age_group = form.get("age_group") or draft.get("age_group")
    if not age_group:
        return redirect(url_for("main.index"))

    demographics = {
        "age_group": age_group,
        "sedentary_lifestyle": form.get("sedentary_lifestyle") == "1",
    }

    answers: dict = {}
    for key in form:
        if key.startswith("q"):
            values = form.getlist(key)
            if key in MULTI_SELECT_IDS or len(values) > 1:
                answers[key] = [int(v) for v in values]
            elif values:
                answers[key] = int(values[0])

    errors = _service().validate(answers)
    if errors:
        sections = _service().get_sections()
        skip = 1 if draft.get("age_group") else 0
        all_steps = flatten_questions(sections)
        active_step = 0
        for i, step in enumerate(all_steps[skip:]):
            if step["id"] in errors:
                active_step = i
                break
        return (
            render_template(
                "questionnaire.html",
                **_quiz_context(
                    sections,
                    errors=errors,
                    form_data=form.to_dict(flat=False),
                    active_step=active_step,
                ),
            ),
            400,
        )

    try:
        result = _service().process(demographics, answers, session.get("assessment_id"))
    except Exception:
        current_app.logger.exception("Assessment processing failed")
        sections = _service().get_sections()
        return (
            render_template(
                "questionnaire.html",
                **_quiz_context(
                    sections,
                    errors={"_form": ["Something went wrong processing your results. Please try again."]},
                    form_data=form.to_dict(flat=False),
                    active_step=0,
                ),
            ),
            500,
        )

    stored = AssessmentService.result_to_dict(result)
    stored["answers"] = answers
    session["assessment"] = stored
    session["assessment_id"] = result.session_id
    session.pop(DRAFT_KEY, None)
    return redirect(url_for("questionnaire.results"))


@questionnaire_bp.route("/results")
def results():
    data = session.get("assessment")
    if not data:
        return redirect(url_for("main.index"))

    ctx = PageLayout.context(active_path="/assessment/", result=data)
    return render_template("results.html", **ctx)


@questionnaire_bp.route("/plan")
def plan():
    data = session.get("assessment")
    if not data:
        return redirect(url_for("main.index"))

    if not data.get("triage", {}).get("includes_kegel_plan"):
        return redirect(url_for("questionnaire.results"))

    plan_html = render_markdown(data.get("customized_plan", ""))
    ctx = PageLayout.context(
        active_path="/assessment/",
        result=data,
        plan_html=plan_html,
    )
    return render_template("plan.html", **ctx)
