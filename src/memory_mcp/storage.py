"""Stockage SQLite + recherche par similarité cosinus (embeddings simplifiés)."""

from __future__ import annotations

import json
import math
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

MIN_SIMILARITY = 1e-9

_STOPWORDS = frozenset(
    {
        "a",
        "au",
        "aux",
        "ce",
        "ces",
        "de",
        "des",
        "du",
        "en",
        "est",
        "et",
        "il",
        "je",
        "la",
        "le",
        "les",
        "ma",
        "mon",
        "ne",
        "on",
        "ou",
        "pas",
        "pour",
        "que",
        "qui",
        "sa",
        "se",
        "son",
        "sur",
        "un",
        "une",
        "vos",
        "votre",
    }
)


@dataclass
class MemoryEntry:
    id: int
    content: str
    tags: list[str]
    session: str
    turn: int
    score: float = 0.0


def _tokenize(text: str) -> dict[str, float]:
    """Bag-of-words normalisé — remplacer par un vrai modèle d'embeddings."""
    words = [w for w in re.findall(r"\w+", text.lower()) if w not in _STOPWORDS and len(w) > 2]
    if not words:
        return {}
    freq: dict[str, float] = {}
    for w in words:
        freq[w] = freq.get(w, 0.0) + 1.0
    norm = math.sqrt(sum(v * v for v in freq.values())) or 1.0
    return {k: v / norm for k, v in freq.items()}


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    return sum(a[k] * b[k] for k in common)


class MemoryStore:
    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                tags TEXT NOT NULL DEFAULT '[]',
                session TEXT NOT NULL DEFAULT 'default',
                turn INTEGER NOT NULL DEFAULT 0,
                embedding TEXT NOT NULL DEFAULT '{}'
            )
            """
        )
        self._conn.commit()

    def store(
        self, content: str, tags: list[str] | None = None, session: str = "default", turn: int = 0
    ) -> int:
        tags = tags or []
        emb = json.dumps(_tokenize(content))
        cur = self._conn.execute(
            "INSERT INTO memories (content, tags, session, turn, embedding) VALUES (?, ?, ?, ?, ?)",
            (content, json.dumps(tags), session, turn, emb),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def search(self, query: str, top_k: int = 5, session: str | None = None) -> list[MemoryEntry]:
        q_vec = _tokenize(query)
        rows = self._conn.execute(
            "SELECT * FROM memories" + (" WHERE session = ?" if session else ""),
            (session,) if session else (),
        ).fetchall()

        scored: list[tuple[float, sqlite3.Row]] = []
        for row in rows:
            vec = json.loads(row["embedding"])
            score = _cosine(q_vec, vec)
            scored.append((score, row))

        scored.sort(key=lambda x: x[0], reverse=True)
        scored = [(s, row) for s, row in scored if s > MIN_SIMILARITY]

        results: list[MemoryEntry] = []
        for score, row in scored[:top_k]:
            results.append(
                MemoryEntry(
                    id=row["id"],
                    content=row["content"],
                    tags=json.loads(row["tags"]),
                    session=row["session"],
                    turn=row["turn"],
                    score=score,
                )
            )
        return results

    def list_session(self, session: str) -> list[MemoryEntry]:
        rows = self._conn.execute(
            "SELECT * FROM memories WHERE session = ? ORDER BY turn ASC, id ASC",
            (session,),
        ).fetchall()
        return [
            MemoryEntry(
                id=r["id"],
                content=r["content"],
                tags=json.loads(r["tags"]),
                session=r["session"],
                turn=r["turn"],
            )
            for r in rows
        ]

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) AS c FROM memories").fetchone()
        return int(row["c"])

    def close(self) -> None:
        self._conn.close()
