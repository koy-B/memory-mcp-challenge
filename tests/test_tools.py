from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools


def test_memory_store():
    reset_stats()
    tools = MemoryTools()
    result = tools.memory_store("Hello world", tags=["test"], session="t1", turn=1)
    assert result["stored"] is True
    assert result["id"] == 1


def test_memory_search():
    reset_stats()
    tools = MemoryTools()
    tools.memory_store("Le client s'appelle Marie Dupont", session="t2", turn=1)
    result = tools.memory_search("nom du client", top_k=1, session="t2")
    assert result["count"] >= 1
    assert "Marie" in result["results"][0]["content"]


def test_memory_summarize():
    reset_stats()
    tools = MemoryTools()
    tools.memory_store("Message 1", session="t3", turn=1)
    tools.memory_store("Message 2", session="t3", turn=2)
    result = tools.memory_summarize(session="t3")
    assert result["source_turns"] == 2
    assert len(result["summary"]) > 0


def test_memory_stats():
    reset_stats()
    tools = MemoryTools()
    tools.memory_store("test")
    stats = tools.memory_stats()
    assert stats["store_calls"] == 1
    assert stats["total_tokens"] > 0
