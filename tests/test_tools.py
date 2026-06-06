"""Tests outils — comportement minimal + sémantique."""

from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools
from memory_mcp.validation import top1_contains


def test_memory_store():
    reset_stats()
    tools = MemoryTools()
    result = tools.memory_store("Hello world", tags=["test"], session="t1", turn=1)
    assert result["stored"] is True
    assert result["id"] == 1


def test_memory_search_semantic():
    """Recherche par paraphrase — pas de mot-clé partagé évident."""
    reset_stats()
    tools = MemoryTools()
    tools.memory_store(
        "L'usager premium s'identifie comme Marie Dupont de TechCorp",
        session="t2",
        turn=1,
    )
    for i in range(15):
        tools.memory_store(f"noise {i} football tennis météo", session="t2", turn=10 + i)

    result = tools.memory_search("qui est l'interlocutrice VIP", top_k=1, session="t2")
    assert result["count"] >= 1
    assert result["results"][0].get("score", 0) > 0.01
    assert top1_contains("Marie Dupont", result["results"])


def test_memory_summarize_compresses():
    reset_stats()
    tools = MemoryTools()
    for i in range(25):
        tools.memory_store(
            f"Message détaillé numéro {i} avec contenu long " * 3, session="t3", turn=i
        )
    result = tools.memory_summarize(session="t3", max_chars=300)
    source_len = sum(len(e.content) for e in tools.store.list_session("t3"))
    assert result["compressed_chars"] / source_len <= 0.2


def test_memory_stats():
    reset_stats()
    tools = MemoryTools()
    tools.memory_store("test")
    stats = tools.memory_stats()
    assert stats["store_calls"] == 1
    assert stats["total_tokens"] > 0
