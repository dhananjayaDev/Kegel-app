"""Standardized PFMT protocol templates."""

from __future__ import annotations

from application.models import Severity


class ProtocolLibrary:
    PROTOCOLS = {
        Severity.NONE: {
            "id": "maintenance",
            "name": "Maintenance Protocol",
            "position": "Standing upright, feet hip-width apart",
            "sets_per_session": 2,
            "daily_frequency": "2 times daily",
            "weekly_cadence": "3 days per week",
            "exercises": [
                {
                    "name": "Standing Isometric Holds",
                    "detail": "70% maximal contraction, 6 sec hold, 12 sec release, 10 reps.",
                },
                {
                    "name": "Standing Quick Flicks",
                    "detail": "10 rapid 1-second contractions with full release.",
                },
            ],
        },
        Severity.MILD: {
            "id": "mild",
            "name": "Protocol 1 — Mild ED Focus",
            "position": "Standing upright with feet hip-width apart",
            "sets_per_session": 2,
            "daily_frequency": "3 times daily (Morning, Noon, Evening)",
            "weekly_cadence": "3 alternating days per week (Mon/Wed/Fri)",
            "exercises": [
                {
                    "name": "Standing Isometric Holds (Type I)",
                    "detail": "70% MVC, hold 6 seconds, release 12 seconds, 12 repetitions.",
                },
                {
                    "name": "Standing Quick Flicks (Type II)",
                    "detail": "10 rapid explosive 1-second squeezes with immediate release.",
                },
                {
                    "name": "Functional Urge Control Knack",
                    "detail": "50% submaximal hold during standing daily activities.",
                },
            ],
        },
        Severity.MILD_MODERATE: {
            "id": "mild_moderate",
            "name": "Protocol 2 — Mild-to-Moderate ED Focus",
            "position": "Seated upright on a hard-backed chair with knees apart",
            "sets_per_session": 3,
            "daily_frequency": "3 times daily",
            "weekly_cadence": "4 days per week",
            "exercises": [
                {
                    "name": "Seated Isometric Holds",
                    "detail": "Maximal squeeze and lift, 8 sec hold, 16 sec release, 10 reps.",
                },
                {
                    "name": "Seated Quick Flicks",
                    "detail": "12 explosive 1-second contractions in a row.",
                },
                {
                    "name": "Active Pelvic Bridges",
                    "detail": "Supine bridge with pelvic floor tension, 5 sec hold, 10 reps.",
                },
            ],
        },
        Severity.MODERATE: {
            "id": "moderate",
            "name": "Protocol 3 — Moderate ED Focus",
            "position": "Lying supine, knees bent, feet flat",
            "sets_per_session": 3,
            "daily_frequency": "3 times daily",
            "weekly_cadence": "5 days per week",
            "exercises": [
                {
                    "name": "Supine Maximal Holds",
                    "detail": "100% MVC, 10 sec hold, 20 sec release, 12 repetitions.",
                },
                {
                    "name": "Supine Quick Flicks",
                    "detail": "15 rapid 1-second squeezes with immediate release.",
                },
                {
                    "name": "Endothelial Walking Program",
                    "detail": "Brisk walk 30 minutes daily, 5 days per week.",
                },
            ],
        },
        Severity.SEVERE: {
            "id": "severe",
            "name": "Protocol 4 — Severe ED Focus (Supportive)",
            "position": "Lying supine, knees bent, pillow under head",
            "sets_per_session": 2,
            "daily_frequency": "2 times daily (Morning and Evening)",
            "weekly_cadence": "3 days per week with rest days",
            "exercises": [
                {
                    "name": "Submaximal Neuromobilization Holds",
                    "detail": "30–50% contraction, 4 sec hold, 12 sec release, 10 reps.",
                },
                {
                    "name": "Diaphragmatic Perineal Release",
                    "detail": "5 minutes deep abdominal breathing, focus on perineal relaxation.",
                },
            ],
        },
    }

    AGE_MODIFIERS = {
        "under_30": "Emphasize fast-twitch quick flicks; younger tissue adapts quickly.",
        "30_39": "Balance endurance holds with functional standing integration.",
        "40_49": "Include daily walking; monitor cardiovascular markers.",
        "50_59": "Start with seated progression before standing; longer rest intervals.",
        "60_plus": "Gentle submaximal holds first; consult physician before high intensity.",
    }

    def for_severity(self, severity: Severity) -> dict:
        return self.PROTOCOLS.get(severity, self.PROTOCOLS[Severity.MODERATE])

    def age_guidance(self, age_group: str) -> str:
        return self.AGE_MODIFIERS.get(age_group, self.AGE_MODIFIERS["40_49"])
