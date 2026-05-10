from __future__ import annotations

import os
from typing import Any

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


class KnowledgeBase:
    def __init__(self, persist_dir: str):
        os.makedirs(persist_dir, exist_ok=True)
        self.persist_dir = persist_dir
        self.embeddings = get_embedding_model()
        self.store = Chroma(
            collection_name="support-kb",
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir,
        )

    def ingest_directory(self, kb_dir: str) -> int:
        docs = []
        for root, _, files in os.walk(kb_dir):
            for filename in files:
                path = os.path.join(root, filename)
                if filename.lower().endswith(".txt"):
                    docs.extend(TextLoader(path, encoding="utf-8").load())
                elif filename.lower().endswith(".pdf"):
                    docs.extend(PyPDFLoader(path).load())

        if not docs:
            return 0

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        chunks = splitter.split_documents(docs)

        if chunks:
            self.store.add_documents(chunks)

        return len(chunks)

    def retrieve(self, query: str, k: int = 4) -> list[dict[str, Any]]:
        docs = self.store.similarity_search(query, k=k)
        results = []
        for d in docs:
            results.append(
                {
                    "content": d.page_content,
                    "source": d.metadata.get("source", "unknown"),
                }
            )
        return results
