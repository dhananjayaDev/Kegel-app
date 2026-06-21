"""Questionnaire data provider."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from application.providers.base import BaseProvider


class QuestionnaireProvider(BaseProvider):
    name = "questionnaire"

    def __init__(self, config: Any) -> None:
        data_dir = Path(getattr(config, "DATA_DIR", "data"))
        path = data_dir / "questions.json"
        with path.open(encoding="utf-8") as fh:
            self._data = json.load(fh)

    def invoke(self, payload: dict[str, Any]) -> Any:
        action = payload.get("action", "sections")
        if action == "sections":
            return self._data["sections"]
        if action == "validate":
            return self.validate_answers(payload.get("answers", {}))
        return self._data

    def validate_answers(self, answers: dict[str, Any]) -> dict[str, list[str]]:
        errors: dict[str, list[str]] = {}
        for section in self._data["sections"]:
            for question in section["questions"]:
                qid = question["id"]
                if not qid.startswith("q"):
                    continue
                if question.get("required", True) and qid not in answers:
                    errors.setdefault(qid, []).append("This question is required.")
                    continue
                if qid not in answers:
                    continue
                value = answers[qid]
                if question["type"] == "multi_select":
                    if not isinstance(value, list) or len(value) == 0:
                        errors.setdefault(qid, []).append("Select at least one option.")
                elif question["type"] in ("single", "likert"):
                    allowed = {opt["value"] for opt in question["options"]}
                    if value not in allowed:
                        errors.setdefault(qid, []).append("Invalid selection.")
        return errors
