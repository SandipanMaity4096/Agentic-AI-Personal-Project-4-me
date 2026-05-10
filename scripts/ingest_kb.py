from __future__ import annotations

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from core.vector_store import KnowledgeBase


if __name__ == "__main__":
    kb = KnowledgeBase(settings.vector_db_path)
    count = kb.ingest_directory(settings.kb_dir)
    print(f"Ingestion complete. Chunks indexed: {count}")
