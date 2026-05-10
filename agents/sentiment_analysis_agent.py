from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent


class SentimentAnalysisAgent(BaseAgent):
    name = "sentiment-analysis-agent"

    NEGATIVE_TERMS = {
        "angry",
        "frustrated",
        "terrible",
        "worst",
        "cancel",
        "disappointed",
        "unacceptable",
        "hate",
        "useless",
        "not happy",
    }

    POSITIVE_TERMS = {"great", "thanks", "awesome", "good", "helpful", "love"}

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = payload.get("user_query", "").lower()

        neg_hits = sum(1 for term in self.NEGATIVE_TERMS if term in text)
        pos_hits = sum(1 for term in self.POSITIVE_TERMS if term in text)

        if neg_hits >= 2:
            sentiment = "very_negative"
        elif neg_hits == 1:
            sentiment = "negative"
        elif pos_hits >= 1 and neg_hits == 0:
            sentiment = "positive"
        else:
            sentiment = "neutral"

        score = pos_hits - neg_hits
        return {"sentiment": sentiment, "score": score}
