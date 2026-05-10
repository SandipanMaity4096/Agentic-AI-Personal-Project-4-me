from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from core.llm import SafeLLM
from core.vector_store import KnowledgeBase


class FAQRetrievalAgent(BaseAgent):
    name = "faq-retrieval-agent"

    def __init__(self, kb: KnowledgeBase, llm: SafeLLM):
        self.kb = kb
        self.llm = llm

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        user_query = payload.get("user_query", "")
        retrieved = self.kb.retrieve(user_query, k=4)

        context = "\n\n".join(
            [f"Source: {r['source']}\n{r['content']}" for r in retrieved]
        )

        system_prompt = (
            "You are a customer support expert. Use only the provided context where possible. "
            "If context is insufficient, respond safely and ask for more detail."
        )
        user_prompt = (
            f"Customer Query:\n{user_query}\n\n"
            f"Retrieved Context:\n{context}\n\n"
            "Provide a concise, empathetic, and actionable response."
        )

        answer = self.llm.ask(system_prompt, user_prompt)

        return {
            "draft_answer": answer,
            "retrieved_docs": retrieved,
        }
