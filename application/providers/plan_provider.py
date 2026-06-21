"""Customized Kegel plan generation provider."""

from __future__ import annotations

from typing import Any

from application.llm.errors import LLMRateLimitError
from application.llm.factory import LLMFactory
from application.models import AssessmentResult, Demographics, ScoringResult, TriageResult
from application.providers.base import BaseProvider
from application.services.protocols import ProtocolLibrary


class PlanGenerator:
    SYSTEM_PROMPT = (
        "You are a clinical pelvic floor exercise coach. Generate a personalized "
        "male Kegel (PFMT) plan based on the assessment data provided. "
        "Use plain language. Structure with markdown headings. Include: "
        "1) Weekly schedule, 2) Daily session breakdown, 3) Age-specific notes, "
        "4) Breathing cues, 5) Progress milestones aligned to clinical timelines. "
        "Do not diagnose or prescribe medication. Add a brief disclaimer that this "
        "is informational only."
    )

    def __init__(self, config: Any) -> None:
        self._config = config
        self._protocols = ProtocolLibrary()
        self._llm = LLMFactory.create(config)

    def base_protocol(self, scoring: ScoringResult) -> dict:
        return self._protocols.for_severity(scoring.severity)

    def _build_template_plan(
        self,
        demographics: Demographics,
        scoring: ScoringResult,
        triage: TriageResult,
        protocol: dict,
    ) -> str:
        age_note = self._protocols.age_guidance(demographics.age_group)
        timeline = triage.timeline
        exercises = "\n".join(
            f"- **{ex['name']}:** {ex['detail']}" for ex in protocol["exercises"]
        )
        milestones = ""
        if timeline:
            milestones = "\n".join(
                f"- **{m['period']}:** {m['note']}" for m in timeline.milestones
            )

        return f"""# Your Customized Kegel Plan

*This plan is for informational purposes only. Consult a healthcare professional for medical advice.*

## Profile Summary
- **Age group:** {demographics.age_group.replace('_', ' ').title()}
- **IIEF-EF score:** {scoring.iief_ef_score}/30 ({scoring.severity.value})
- **Primary profile:** {scoring.primary_etiology.value if scoring.primary_etiology else 'Mixed'}
- **Pathway:** {triage.title}

## Base Protocol — {protocol['name']}
- **Position:** {protocol['position']}
- **Sets per session:** {protocol['sets_per_session']}
- **Daily frequency:** {protocol['daily_frequency']}
- **Weekly cadence:** {protocol['weekly_cadence']}

## Exercises
{exercises}

## Age-Specific Guidance
{age_note}

## Somatic Cue
Voluntarily contract your pelvic floor as if stopping urine mid-stream and holding in gas.
Avoid tensing abdomen, buttocks, or holding your breath.

## Expected Timeline
- **First noticeable changes:** {timeline.first_notice_weeks if timeline else '4–6'} weeks
- **Peak improvement window:** {timeline.peak_improvement_weeks if timeline else '8–12'} weeks
- **Full evaluation period:** {timeline.full_evaluation_months if timeline else '6'} months
- **Clinical reference:** {timeline.resolution_rate if timeline else 'Individual results vary'}

### Milestones
{milestones}
"""

    def _build_llm_prompt(
        self,
        demographics: Demographics,
        scoring: ScoringResult,
        triage: TriageResult,
        protocol: dict,
        answers: dict[str, Any],
    ) -> str:
        return (
            f"Demographics: age_group={demographics.age_group}, "
            f"sedentary={demographics.sedentary_lifestyle}\n"
            f"IIEF-EF score: {scoring.iief_ef_score}, severity: {scoring.severity.value}\n"
            f"Etiologies: {[e.value for e in scoring.etiologies]}\n"
            f"Pathway: {triage.pathway.value} — {triage.title}\n"
            f"Morning erections (Q17): {answers.get('q17')}\n"
            f"Onset pattern (Q16): {answers.get('q16')}\n"
            f"Base protocol JSON: {protocol}\n"
            f"Timeline: peak {triage.timeline.peak_improvement_weeks if triage.timeline else '12'} weeks\n"
            "Personalize session timing, rest days, and progression for this user."
        )

    def generate(
        self,
        demographics: Demographics,
        answers: dict[str, Any],
        scoring: ScoringResult,
        triage: TriageResult,
    ) -> tuple[str, str, dict, bool]:
        protocol = self.base_protocol(scoring)
        template = self._build_template_plan(demographics, scoring, triage, protocol)

        if not self._llm:
            return template, "template", protocol, False

        try:
            customized = self._llm.generate(
                self.SYSTEM_PROMPT,
                self._build_llm_prompt(demographics, scoring, triage, protocol, answers),
            )
            if customized:
                return customized, self._config.LLM_PROVIDER, protocol, False
        except LLMRateLimitError:
            return template, "template (rate limited)", protocol, True
        except Exception:
            pass

        return template, "template (LLM unavailable)", protocol, False


class PlanProvider(BaseProvider):
    name = "plan"

    def __init__(self, config: Any) -> None:
        self._generator = PlanGenerator(config)

    def invoke(self, payload: dict[str, Any]) -> dict[str, Any]:
        demographics = payload["demographics"]
        if not isinstance(demographics, Demographics):
            demographics = Demographics(**demographics)

        scoring = payload["scoring"]
        triage = payload["triage"]
        answers = payload["answers"]

        plan_text, source, protocol, llm_rate_limited = self._generator.generate(
            demographics, answers, scoring, triage
        )
        return {
            "customized_plan": plan_text,
            "plan_source": source,
            "base_protocol": protocol,
            "llm_rate_limited": llm_rate_limited,
        }
