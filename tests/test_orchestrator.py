from agents.escalation_agent import EscalationAgent
from agents.sentiment_analysis_agent import SentimentAnalysisAgent


def test_sentiment_negative():
    agent = SentimentAnalysisAgent()
    result = agent.run({"user_query": "I am very frustrated and this is terrible"})
    assert result["sentiment"] in {"negative", "very_negative"}


def test_escalation_trigger_for_very_negative():
    agent = EscalationAgent()
    result = agent.run(
        {
            "user_query": "This is unacceptable. I want a manager now.",
            "sentiment": "very_negative",
            "intent": "general",
        }
    )
    assert result["escalate"] is True
