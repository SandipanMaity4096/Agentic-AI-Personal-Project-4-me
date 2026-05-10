from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from core.config import settings


class LLMFactory:
    @staticmethod
    def build_chat_model(provider: str | None = None) -> BaseChatModel:
        selected = (provider or settings.llm_provider).lower()

        if selected == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=settings.openai_model,
                api_key=settings.openai_api_key,
                temperature=0.2,
            )

        if selected == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.google_api_key,
                temperature=0.2,
            )

        if selected == "ollama":
            from langchain_ollama import ChatOllama

            return ChatOllama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0.2,
            )

        raise ValueError(f"Unsupported LLM provider: {selected}")


class SafeLLM:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.llm_provider
        try:
            self.model = LLMFactory.build_chat_model(self.provider)
            self.available = True
        except Exception:
            self.model = None
            self.available = False

    def ask(self, system_prompt: str, user_prompt: str) -> str:
        if not self.available:
            return (
                "I am running in fallback mode. Configure your LLM API key to enable "
                "fully generated answers."
            )

        response = self.model.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        )
        return str(response.content)
