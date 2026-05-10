from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from core.llm import SafeLLM


class CustomerQueryAgent(BaseAgent):
    name = "customer-query-agent"

    def __init__(self, llm: SafeLLM):
        self.llm = llm

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        user_query = payload.get("user_query", "")

        system_prompt = (
            "You classify customer support queries. Return a compact JSON-like response with: "
            "intent, urgency, product_area. Intent can be: billing, technical_issue, refund, "
            "account, delivery, general."
        )

        answer = self.llm.ask(system_prompt, user_query)

        lowered = user_query.lower()
        heuristic_intent = "general"
        if any(word in lowered for word in ["refund", "money back", "charge"]):
            heuristic_intent = "refund"
        elif any(word in lowered for word in ["invoice", "billing", "payment"]):
            heuristic_intent = "billing"
        elif any(word in lowered for word in ["error", "bug", "crash", "not working"]):
            heuristic_intent = "technical_issue"
        elif any(word in lowered for word in ["login", "password", "account"]):
            heuristic_intent = "account"
        elif any(word in lowered for word in ["delivery", "shipment", "order status"]):
            heuristic_intent = "delivery"

        urgency = "normal"
        if any(word in lowered for word in ["urgent", "asap", "immediately", "now"]):
            urgency = "high"

        return {
            "intent": heuristic_intent,
            "urgency": urgency,
            "raw_classification": answer,
        }
