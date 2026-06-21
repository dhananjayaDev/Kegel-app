"""Clinical scoring and etiology mapping engine."""

from __future__ import annotations

from typing import Any

from application.models import Demographics, Etiology, ScoringResult, Severity
from application.providers.base import BaseProvider


class ScoringEngine:
    EF_QUESTIONS = ("q1", "q2", "q3", "q4", "q5", "q15")

    def calculate_iief_ef(self, answers: dict[str, Any]) -> int:
        total = 0
        for qid in self.EF_QUESTIONS:
            total += int(answers.get(qid, 0))
        return total

    def classify_severity(self, score: int) -> Severity:
        if score >= 26:
            return Severity.NONE
        if score >= 22:
            return Severity.MILD
        if score >= 17:
            return Severity.MILD_MODERATE
        if score >= 11:
            return Severity.MODERATE
        return Severity.SEVERE

    def map_etiologies(self, answers: dict[str, Any]) -> list[Etiology]:
        found: list[Etiology] = []
        q2 = int(answers.get("q2", 0))
        q4 = int(answers.get("q4", 0))
        q16 = int(answers.get("q16", 0))
        q17 = int(answers.get("q17", 0))
        q18 = int(answers.get("q18", 0))
        q20 = int(answers.get("q20", 0))
        q22 = answers.get("q22", [])
        q26 = int(answers.get("q26", 1))
        q28 = int(answers.get("q28", 1))
        q29 = int(answers.get("q29", 1))
        q30 = int(answers.get("q30", 1))
        q11 = int(answers.get("q11", 3))
        q12 = int(answers.get("q12", 3))

        psychogenic = q16 == 1 and q17 >= 4 and q18 == 1
        organic = q16 == 0 or q17 <= 1
        vascular_comorbidity = isinstance(q22, list) and 0 in q22

        if q30 == 0:
            found.append(Etiology.ANATOMICAL)
        if q28 == 0 or q29 == 0:
            found.append(Etiology.NEUROGENIC)
        if (q11 <= 2 and q12 <= 2) and q26 == 0:
            found.append(Etiology.ENDOCRINOPATHIC)
        if psychogenic:
            found.append(Etiology.PSYCHOGENIC)
        if organic:
            if q2 < q4 or vascular_comorbidity:
                found.append(Etiology.ARTERIOGENIC)
            if q4 < q2 or q20 == 0:
                found.append(Etiology.VENOGENIC)

        if psychogenic and organic and Etiology.MIXED not in found:
            found.append(Etiology.MIXED)

        if not found:
            found.append(Etiology.MIXED)

        return list(dict.fromkeys(found))

    def primary_etiology(self, etiologies: list[Etiology]) -> Etiology:
        priority = [
            Etiology.ANATOMICAL,
            Etiology.NEUROGENIC,
            Etiology.ENDOCRINOPATHIC,
            Etiology.PSYCHOGENIC,
            Etiology.VENOGENIC,
            Etiology.ARTERIOGENIC,
            Etiology.MIXED,
        ]
        for item in priority:
            if item in etiologies:
                return item
        return etiologies[0]

    def evaluate(
        self, answers: dict[str, Any], demographics: Demographics | None = None
    ) -> ScoringResult:
        score = self.calculate_iief_ef(answers)
        severity = self.classify_severity(score)
        etiologies = self.map_etiologies(answers)
        return ScoringResult(
            iief_ef_score=score,
            severity=severity,
            etiologies=etiologies,
            primary_etiology=self.primary_etiology(etiologies),
        )


class ScoringProvider(BaseProvider):
    name = "scoring"

    def __init__(self) -> None:
        self._engine = ScoringEngine()

    def invoke(self, payload: dict[str, Any]) -> ScoringResult:
        answers = payload["answers"]
        demographics = payload.get("demographics")
        if demographics and not isinstance(demographics, Demographics):
            demographics = Demographics(**demographics)
        return self._engine.evaluate(answers, demographics)
