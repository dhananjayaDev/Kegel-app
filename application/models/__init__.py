"""Domain models for assessment pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    NONE = "No Erectile Dysfunction"
    MILD = "Mild ED"
    MILD_MODERATE = "Mild-to-Moderate ED"
    MODERATE = "Moderate ED"
    SEVERE = "Severe ED"


class Etiology(str, Enum):
    PSYCHOGENIC = "Psychogenic"
    ARTERIOGENIC = "Arteriogenic"
    VENOGENIC = "Venogenic / Muscular Weakness"
    NEUROGENIC = "Neurogenic"
    ENDOCRINOPATHIC = "Endocrinopathic"
    ANATOMICAL = "Anatomical / Structural"
    MIXED = "Mixed ED"


class Pathway(str, Enum):
    PFMT = "A"
    CBT = "B"
    UROLOGY = "C"
    CARDIOLOGY = "D"
    EMERGENCY = "E"
    COMBINED_MEDICAL = "C+A"
    PFMT_METABOLIC = "A+D"


@dataclass
class Demographics:
    age_group: str
    sedentary_lifestyle: bool = False


@dataclass
class ScoringResult:
    iief_ef_score: int
    severity: Severity
    etiologies: list[Etiology] = field(default_factory=list)
    primary_etiology: Etiology | None = None


@dataclass
class TimelineEstimate:
    first_notice_weeks: str
    peak_improvement_weeks: str
    full_evaluation_months: str
    resolution_rate: str
    milestones: list[dict[str, str]] = field(default_factory=list)


@dataclass
class TriageResult:
    pathway: Pathway
    title: str
    message: str
    action_items: list[str]
    includes_kegel_plan: bool
    urgency: str  # normal | elevated | critical
    timeline: TimelineEstimate | None = None


@dataclass
class AssessmentResult:
    session_id: str
    demographics: Demographics
    answers: dict[str, Any]
    scoring: ScoringResult
    triage: TriageResult
    base_protocol: dict[str, Any] | None = None
    customized_plan: str | None = None
    plan_source: str = "template"
