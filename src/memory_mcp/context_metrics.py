"""Métriques de contexte LLM partagées entre benchmark et dashboard live."""

from __future__ import annotations

from typing import TYPE_CHECKING

from memory_mcp.stats import count_tokens

if TYPE_CHECKING:
    from memory_mcp.tools import MemoryTools


def compact_snippet(content: str, max_len: int = 44) -> str:
    text = content.strip()
    text = text.split(":", 1)[-1].strip() if ":" in text else text
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def per_turn_context_tokens(tools: MemoryTools, session: str, query: str) -> int:
    """Tokens du contexte LLM pour un tour (résumé + 1 souvenir pertinent)."""
    summary = tools.memory_summarize(session=session, max_chars=150)
    search = tools.memory_search(query=query, top_k=1, session=session)
    snippets = [compact_snippet(r["content"]) for r in search["results"]]
    context = summary["summary"]
    if snippets:
        context = f"{context}\n{snippets[0]}" if context else snippets[0]
    return count_tokens(context)
