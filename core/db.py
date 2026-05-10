from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from typing import Any


class SupportDB:
    def __init__(self, db_path: str):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                sentiment TEXT,
                intent TEXT,
                agent_trace TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_query TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    def save_message(
        self,
        session_id: str,
        role: str,
        message: str,
        sentiment: str | None = None,
        intent: str | None = None,
        agent_trace: dict[str, Any] | None = None,
    ) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO conversations (session_id, role, message, sentiment, intent, agent_trace, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                role,
                message,
                sentiment,
                intent,
                json.dumps(agent_trace or {}),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

    def get_history(self, session_id: str, limit: int = 12) -> list[dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT role, message, sentiment, intent, created_at
            FROM conversations
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        )
        rows = cur.fetchall()
        conn.close()

        rows = list(reversed(rows))
        return [dict(r) for r in rows]

    def create_ticket(
        self,
        session_id: str,
        user_query: str,
        reason: str,
        priority: str = "high",
    ) -> int:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO tickets (session_id, user_query, reason, status, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                user_query,
                reason,
                "open",
                priority,
                datetime.utcnow().isoformat(),
            ),
        )
        ticket_id = cur.lastrowid
        conn.commit()
        conn.close()
        return int(ticket_id)

    def list_tickets(self) -> list[dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, session_id, reason, priority, status, created_at
            FROM tickets
            ORDER BY id DESC
            """
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows
