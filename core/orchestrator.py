from __future__ import annotations

from typing import Any

from agents.customer_query_agent import CustomerQueryAgent
from agents.escalation_agent import EscalationAgent
from agents.faq_retrieval_agent import FAQRetrievalAgent
from agents.sentiment_analysis_agent import SentimentAnalysisAgent
from core.db import SupportDB
from core.llm import SafeLLM
from core.vector_store import KnowledgeBase


class AgentOrchestrator:
    def __init__(self, db: SupportDB, kb: KnowledgeBase, llm_provider: str):
        llm = SafeLLM(provider=llm_provider)
        self.db = db
        self.query_agent = CustomerQueryAgent(llm)
        self.sentiment_agent = SentimentAnalysisAgent()
        self.faq_agent = FAQRetrievalAgent(kb, llm)
        self.escalation_agent = EscalationAgent()

    def handle(self, session_id: str, user_query: str) -> dict[str, Any]:
        query_result = self.query_agent.run({"user_query": user_query})
        sentiment_result = self.sentiment_agent.run({"user_query": user_query})

        rag_result = self.faq_agent.run({"user_query": user_query})

        escalation_result = self.escalation_agent.run(
            {
                "user_query": user_query,
                "intent": query_result["intent"],
                "sentiment": sentiment_result["sentiment"],
            }
        )

        final_response = rag_result["draft_answer"]
        ticket_id = None

        if escalation_result["escalate"]:
            ticket_id = self.db.create_ticket(
                session_id=session_id,
                user_query=user_query,
                reason=escalation_result["reason"],
                priority=escalation_result["priority"],
            )
            final_response += (
                "\n\nI have escalated this to a human support specialist. "
                f"Your ticket ID is #{ticket_id}."
            )

        trace = {
            "query_agent": query_result,
            "sentiment_agent": sentiment_result,
            "faq_agent_docs": rag_result["retrieved_docs"],
            "escalation_agent": escalation_result,
            "ticket_id": ticket_id,
        }

        self.db.save_message(
            session_id=session_id,
            role="user",
            message=user_query,
            sentiment=sentiment_result["sentiment"],
            intent=query_result["intent"],
        )
        self.db.save_message(
            session_id=session_id,
            role="assistant",
            message=final_response,
            sentiment=sentiment_result["sentiment"],
            intent=query_result["intent"],
            agent_trace=trace,
        )

        return {
            "response": final_response,
            "trace": trace,
        }
