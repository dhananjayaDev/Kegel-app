"""Clinical triage and pathway routing engine."""

from __future__ import annotations

from typing import Any

from application.models import (
    Etiology,
    Pathway,
    ScoringResult,
    Severity,
    TimelineEstimate,
    TriageResult,
)
from application.providers.base import BaseProvider
from application.services.protocols import ProtocolLibrary


class TriageEngine:
    def __init__(self) -> None:
        self._protocols = ProtocolLibrary()

    def _timeline_for(self, severity: Severity) -> TimelineEstimate:
        timelines = {
            Severity.NONE: TimelineEstimate(
                first_notice_weeks="1–2",
                peak_improvement_weeks="4–6",
                full_evaluation_months="3",
                resolution_rate="Maintenance only",
                milestones=[
                    {"period": "Weeks 1–2", "note": "Muscle awareness and coordination."},
                    {"period": "Weeks 6–8", "note": "Sustain existing function."},
                ],
            ),
            Severity.MILD: TimelineEstimate(
                first_notice_weeks="2–3",
                peak_improvement_weeks="8–12",
                full_evaluation_months="6",
                resolution_rate="40% full resolution; 34.5% significant improvement at 6 months",
                milestones=[
                    {"period": "Weeks 1–2", "note": "Improved pelvic floor awareness."},
                    {"period": "Weeks 3–4", "note": "Strength and endurance gains."},
                    {"period": "Weeks 6–8", "note": "Noticeable rigidity improvements."},
                    {"period": "Weeks 8–12", "note": "Peak muscular hypertrophy milestone."},
                    {"period": "6 Months", "note": "Long-term resolution window (Dorey RCT)."},
                ],
            ),
            Severity.MILD_MODERATE: TimelineEstimate(
                first_notice_weeks="3–4",
                peak_improvement_weeks="10–14",
                full_evaluation_months="6",
                resolution_rate="Up to 67% mild-to-moderate cases improve by 12 weeks",
                milestones=[
                    {"period": "Weeks 1–2", "note": "Base neural activation."},
                    {"period": "Weeks 4–6", "note": "Progressive loading gains."},
                    {"period": "Weeks 8–12", "note": "Functional integration."},
                    {"period": "6 Months", "note": "Reassess IIEF-EF domain."},
                ],
            ),
            Severity.MODERATE: TimelineEstimate(
                first_notice_weeks="4–6",
                peak_improvement_weeks="12–16",
                full_evaluation_months="6–9",
                resolution_rate="Combined PFMT + metabolic coaching recommended",
                milestones=[
                    {"period": "Weeks 1–2", "note": "Supine neuromobilization."},
                    {"period": "Weeks 6–8", "note": "Seated progressive loading."},
                    {"period": "Weeks 12+", "note": "Standing functional integration."},
                    {"period": "6–9 Months", "note": "Medical co-management if plateau."},
                ],
            ),
            Severity.SEVERE: TimelineEstimate(
                first_notice_weeks="6–8",
                peak_improvement_weeks="16–24",
                full_evaluation_months="6–12",
                resolution_rate="Requires urological co-management; PFMT as supportive care",
                milestones=[
                    {"period": "Weeks 1–4", "note": "Gentle submaximal holds only."},
                    {"period": "Weeks 8–12", "note": "Gradual intensity increase if tolerated."},
                    {"period": "6+ Months", "note": "Specialist follow-up essential."},
                ],
            ),
        }
        return timelines[severity]

    def route(self, answers: dict[str, Any], scoring: ScoringResult) -> TriageResult:
        q31 = int(answers.get("q31", 1))
        q32 = int(answers.get("q32", 1))
        q28 = int(answers.get("q28", 1))
        q30 = int(answers.get("q30", 1))
        q23 = int(answers.get("q23", 1))
        q22 = answers.get("q22", [])
        vascular = isinstance(q22, list) and 0 in q22

        timeline = self._timeline_for(scoring.severity)

        if q32 == 0 or q31 == 0:
            return TriageResult(
                pathway=Pathway.EMERGENCY,
                title="Emergency Alert",
                message=(
                    "Suspected ischemic priapism or acute pelvic trauma detected. "
                    "Go to the nearest Emergency Department (A&E) immediately."
                ),
                action_items=[
                    "Do not wait for symptoms to resolve on their own.",
                    "Seek emergency urological care for priapism lasting over 4 hours.",
                    "Inform clinicians about any recent pelvic or groin trauma.",
                ],
                includes_kegel_plan=False,
                urgency="critical",
                timeline=timeline,
            )

        if q30 == 0 or q28 == 0:
            return TriageResult(
                pathway=Pathway.UROLOGY,
                title="Urology Referral Required",
                message=(
                    "A physician must examine your pelvic nerves or penile anatomy "
                    "to evaluate conditions such as Peyronie's disease or nerve injury."
                ),
                action_items=[
                    "Schedule a urology consultation promptly.",
                    "Do not start intensive pelvic training without clearance.",
                    "Bring this assessment summary to your appointment.",
                ],
                includes_kegel_plan=False,
                urgency="elevated",
                timeline=timeline,
            )

        if vascular or q23 == 0:
            return TriageResult(
                pathway=Pathway.CARDIOLOGY,
                title="Cardiovascular Screening Recommended",
                message=(
                    "Erectile dysfunction can be an early warning sign for cardiovascular disease. "
                    "Please undergo cardiology evaluation before starting intensive exercise "
                    "(Princeton III Consensus)."
                ),
                action_items=[
                    "Request a cardiology or primary care cardiovascular risk assessment.",
                    "Discuss exercise tolerance and MET capacity with your clinician.",
                    "Begin only gentle pelvic floor awareness until cleared.",
                ],
                includes_kegel_plan=scoring.iief_ef_score >= 11,
                urgency="elevated",
                timeline=timeline,
            )

        if scoring.iief_ef_score <= 10:
            return TriageResult(
                pathway=Pathway.COMBINED_MEDICAL,
                title="Combined Medical & Urological Care",
                message=(
                    "Severe erectile dysfunction warrants urological consultation for "
                    "first-line medical options, alongside gentle pelvic floor mobilization."
                ),
                action_items=[
                    "Consult a urologist about PDE5 inhibitors and root-cause workup.",
                    "Use the gentle base-mobilization PFMT protocol as supportive care.",
                    "Screen lipids, HbA1c, and testosterone with your clinician.",
                ],
                includes_kegel_plan=True,
                urgency="elevated",
                timeline=timeline,
            )

        primary = scoring.primary_etiology
        score = scoring.iief_ef_score

        if (
            primary == Etiology.PSYCHOGENIC
            and 11 <= score <= 25
            and Etiology.MIXED not in scoring.etiologies
        ):
            return TriageResult(
                pathway=Pathway.CBT,
                title="Cognitive Behavioral / Sex Therapy Pathway",
                message=(
                    "Your profile suggests a primarily psychogenic component. "
                    "Psychosexual therapy or digital CBT can reduce performance anxiety, "
                    "with a light Kegel routine to build physical confidence."
                ),
                action_items=[
                    "Consider licensed psychosexual therapy or CBT modules.",
                    "Practice mindfulness before intimacy.",
                    "Follow the light supplemental Kegel plan provided.",
                ],
                includes_kegel_plan=True,
                urgency="normal",
                timeline=timeline,
            )

        if (
            17 <= score <= 25
            and primary == Etiology.VENOGENIC
            and scoring.severity != Severity.NONE
        ):
            return TriageResult(
                pathway=Pathway.PFMT,
                title="Pelvic Floor Muscle Training (PFMT)",
                message=(
                    "Venous-leak-related erectile dysfunction is highly responsive to "
                    "supervised pelvic floor muscle training. Your profile indicates PFMT "
                    "as the primary non-pharmacological intervention."
                ),
                action_items=[
                    "Follow your customized Kegel exercise plan daily.",
                    "Perform sessions 3 times daily on scheduled training days.",
                    "Track weekly progress and reassess at 12 weeks.",
                ],
                includes_kegel_plan=True,
                urgency="normal",
                timeline=timeline,
            )

        if 11 <= score <= 16:
            return TriageResult(
                pathway=Pathway.PFMT_METABOLIC,
                title="PFMT & Metabolic Coaching",
                message=(
                    "Mixed or organic erectile dysfunction in the mild-to-moderate range "
                    "benefits from structured PFMT paired with metabolic health optimization."
                ),
                action_items=[
                    "Request primary care screening for lipids and HbA1c.",
                    "Walk briskly 30 minutes daily, 5 days per week.",
                    "Follow the moderate-intensity PFMT protocol below.",
                ],
                includes_kegel_plan=True,
                urgency="normal",
                timeline=timeline,
            )

        if score >= 22 and scoring.severity in (Severity.MILD, Severity.NONE):
            return TriageResult(
                pathway=Pathway.PFMT,
                title="Preventive Pelvic Floor Training",
                message=(
                    "Your erectile function scores are near-normal. A standing PFMT "
                    "maintenance protocol can preserve veno-occlusive strength."
                ),
                action_items=[
                    "Complete the mild ED maintenance protocol.",
                    "Maintain aerobic activity 150 minutes per week.",
                    "Reassess in 12 weeks if symptoms change.",
                ],
                includes_kegel_plan=True,
                urgency="normal",
                timeline=timeline,
            )

        return TriageResult(
            pathway=Pathway.PFMT_METABOLIC,
            title="Structured PFMT Program",
            message=(
                "Based on your assessment, a progressive pelvic floor training program "
                "combined with lifestyle optimization is recommended."
            ),
            action_items=[
                "Follow the customized exercise plan.",
                "Maintain consistent daily practice.",
                "Consult a clinician if no improvement by 12 weeks.",
            ],
            includes_kegel_plan=True,
            urgency="normal",
            timeline=timeline,
        )


class TriageProvider(BaseProvider):
    name = "triage"

    def __init__(self) -> None:
        self._engine = TriageEngine()

    def invoke(self, payload: dict[str, Any]) -> TriageResult:
        return self._engine.route(payload["answers"], payload["scoring"])
