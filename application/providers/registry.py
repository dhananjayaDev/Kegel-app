"""Central provider registry."""

from __future__ import annotations

from typing import Any

from application.providers.base import BaseProvider


class ProviderRegistry:
    """Central dispatcher for assessment pipeline providers."""

    def __init__(self, config: dict[str, Any] | Any) -> None:
        from application.providers.plan_provider import PlanProvider
        from application.providers.questionnaire_provider import QuestionnaireProvider
        from application.providers.scoring_provider import ScoringProvider
        from application.providers.triage_provider import TriageProvider

        self._config = config
        self._providers: dict[str, BaseProvider] = {
            "questionnaire": QuestionnaireProvider(config),
            "scoring": ScoringProvider(),
            "triage": TriageProvider(),
            "plan": PlanProvider(config),
        }

    def get(self, name: str) -> BaseProvider:
        if name not in self._providers:
            raise KeyError(f"Unknown provider: {name}")
        return self._providers[name]

    def invoke(self, name: str, payload: dict[str, Any]) -> Any:
        return self.get(name).invoke(payload)
