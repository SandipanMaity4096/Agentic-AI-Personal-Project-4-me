from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent


class EscalationAgent(BaseAgent):
    name = "escalation-agent"

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        sentiment = payload.get("sentiment", "neutral")
        intent = payload.get("intent", "general")
        user_query = payload.get("user_query", "").lower()

        escalate_keywords = [
            "manager",
            "legal",
            "complaint",
            "cancel my account",
            "chargeback",
            "consumer court",
        ]

        should_escalate = sentiment in {"very_negative"} or any(
            k in user_query for k in escalate_keywords
        )

        reason = "no escalation needed"
        priority = "normal"

        if should_escalate:
            reason = "High dissatisfaction or critical customer request"
            priority = "high"
        elif intent in {"refund", "billing"} and "urgent" in user_query:
            should_escalate = True
            reason = "Urgent finance-related issue"
            priority = "high"

        return {
            "escalate": should_escalate,
            "reason": reason,
            "priority": priority,
        }
