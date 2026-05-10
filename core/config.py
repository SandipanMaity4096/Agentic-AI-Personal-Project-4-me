from dataclasses import dataclass
from dotenv import load_dotenv
import os


load_dotenv()


@dataclass
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "storage/vector_db")
    sqlite_db_path: str = os.getenv("SQLITE_DB_PATH", "storage/support_bot.db")
    kb_dir: str = os.getenv("KB_DIR", "data/knowledge_base")


settings = Settings()
