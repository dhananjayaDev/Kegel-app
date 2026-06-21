"""Questionnaire helpers."""

from __future__ import annotations

from typing import Any


def flatten_questions(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten sectioned questionnaire into a single ordered step list."""
    steps: list[dict[str, Any]] = []
    for section in sections:
        for index, question in enumerate(section["questions"]):
            steps.append(
                {
                    **question,
                    "section_id": section["id"],
                    "section_title": section["title"],
                    "section_description": section.get("description", ""),
                    "is_first_in_section": index == 0,
                }
            )
    return steps


def first_question(sections: list[dict[str, Any]]) -> dict[str, Any] | None:
    steps = flatten_questions(sections)
    return steps[0] if steps else None


def options_side_by_side(options: list[dict[str, Any]]) -> bool:
    """Use a 2-column grid only for plain Yes / No pairs."""
    if len(options) != 2:
        return False
    labels = {str(opt.get("label", "")).strip().lower() for opt in options}
    return labels == {"no", "yes"}
