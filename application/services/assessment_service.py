"""Assessment orchestration service."""

from __future__ import annotations

import uuid
from typing import Any

from application.models import AssessmentResult, Demographics
from application.providers.registry import ProviderRegistry


class AssessmentService:
    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def get_sections(self) -> list[dict[str, Any]]:
        return self._registry.invoke("questionnaire", {"action": "sections"})

    def validate(self, answers: dict[str, Any]) -> dict[str, list[str]]:
        return self._registry.invoke("questionnaire", {"action": "validate", "answers": answers})

    def process(
        self,
        demographics: dict[str, Any],
        answers: dict[str, Any],
        session_id: str | None = None,
    ) -> AssessmentResult:
        demo = Demographics(
            age_group=demographics["age_group"],
            sedentary_lifestyle=demographics.get("sedentary_lifestyle", False),
        )

        scoring = self._registry.invoke(
            "scoring", {"answers": answers, "demographics": demo}
        )
        triage = self._registry.invoke(
            "triage", {"answers": answers, "scoring": scoring}
        )

        plan_data: dict[str, Any] = {}
        if triage.includes_kegel_plan:
            plan_data = self._registry.invoke(
                "plan",
                {
                    "demographics": demo,
                    "answers": answers,
                    "scoring": scoring,
                    "triage": triage,
                },
            )

        return AssessmentResult(
            session_id=session_id or str(uuid.uuid4()),
            demographics=demo,
            answers=answers,
            scoring=scoring,
            triage=triage,
            base_protocol=plan_data.get("base_protocol"),
            customized_plan=plan_data.get("customized_plan"),
            plan_source=plan_data.get("plan_source", "template"),
        )

    @staticmethod
    def result_to_dict(result: AssessmentResult) -> dict[str, Any]:
        timeline = result.triage.timeline
        return {
            "session_id": result.session_id,
            "demographics": {
                "age_group": result.demographics.age_group,
                "sedentary_lifestyle": result.demographics.sedentary_lifestyle,
            },
            "scoring": {
                "iief_ef_score": result.scoring.iief_ef_score,
                "severity": result.scoring.severity.value,
                "etiologies": [e.value for e in result.scoring.etiologies],
                "primary_etiology": (
                    result.scoring.primary_etiology.value
                    if result.scoring.primary_etiology
                    else None
                ),
            },
            "triage": {
                "pathway": result.triage.pathway.value,
                "title": result.triage.title,
                "message": result.triage.message,
                "action_items": result.triage.action_items,
                "includes_kegel_plan": result.triage.includes_kegel_plan,
                "urgency": result.triage.urgency,
                "timeline": {
                    "first_notice_weeks": timeline.first_notice_weeks,
                    "peak_improvement_weeks": timeline.peak_improvement_weeks,
                    "full_evaluation_months": timeline.full_evaluation_months,
                    "resolution_rate": timeline.resolution_rate,
                    "milestones": timeline.milestones,
                }
                if timeline
                else None,
            },
            "base_protocol": result.base_protocol,
            "customized_plan": result.customized_plan,
            "plan_source": result.plan_source,
        }

    @staticmethod
    def result_from_dict(data: dict[str, Any]) -> AssessmentResult:
        from application.models import Etiology, Pathway, ScoringResult, Severity, TimelineEstimate, TriageResult

        scoring_data = data["scoring"]
        triage_data = data["triage"]
        timeline_data = triage_data.get("timeline")

        timeline = None
        if timeline_data:
            timeline = TimelineEstimate(**timeline_data)

        return AssessmentResult(
            session_id=data["session_id"],
            demographics=Demographics(**data["demographics"]),
            answers=data.get("answers", {}),
            scoring=ScoringResult(
                iief_ef_score=scoring_data["iief_ef_score"],
                severity=Severity(scoring_data["severity"]),
                etiologies=[Etiology(e) for e in scoring_data["etiologies"]],
                primary_etiology=(
                    Etiology(scoring_data["primary_etiology"])
                    if scoring_data.get("primary_etiology")
                    else None
                ),
            ),
            triage=TriageResult(
                pathway=Pathway(triage_data["pathway"]),
                title=triage_data["title"],
                message=triage_data["message"],
                action_items=triage_data["action_items"],
                includes_kegel_plan=triage_data["includes_kegel_plan"],
                urgency=triage_data["urgency"],
                timeline=timeline,
            ),
            base_protocol=data.get("base_protocol"),
            customized_plan=data.get("customized_plan"),
            plan_source=data.get("plan_source", "template"),
        )
