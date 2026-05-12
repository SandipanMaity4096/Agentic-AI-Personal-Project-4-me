from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from core.config import settings

# Gracefully imported — only present when langchain_google_genai is installed
try:
    from google.api_core.exceptions import NotFound as _GoogleNotFound
    from google.api_core.exceptions import ResourceExhausted as _GoogleQuotaError
except ImportError:  # pragma: no cover
    _GoogleNotFound = None
    _GoogleQuotaError = None



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

        try:
            response = self.model.invoke(
                [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            )
            return str(response.content)
        except Exception as exc:
            exc_type = type(exc).__name__
            exc_str = str(exc)

            # Quota / rate-limit exceeded
            if _GoogleQuotaError and isinstance(exc, _GoogleQuotaError):
                return (
                    "⚠️ The Gemini API quota has been exhausted for this API key. "
                    "Please wait a few minutes and try again, or switch to a different "
                    "LLM provider in the sidebar."
                )

            # Model not found / deprecated
            if _GoogleNotFound and isinstance(exc, _GoogleNotFound):
                return (
                    f"⚠️ The configured Gemini model was not found: {exc_str}. "
                    "Please update GEMINI_MODEL in your .env file."
                )

            # Generic fallback — surface the error message without a full traceback
            if "ResourceExhausted" in exc_type or "429" in exc_str:
                return (
                    "⚠️ API quota exceeded. Please retry in a moment or switch to "
                    "another LLM provider."
                )

            raise
