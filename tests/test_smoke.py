"""Tests fumée — vérifient que l'API existe (passent avec le squelette)."""

from memory_mcp.tools import MemoryTools
from memory_mcp.validation import assert_integrity


def test_integrity_marker():
    assert_integrity()


def test_tools_api_surface():
    tools = MemoryTools()
    assert tools.memory_store("ping", session="smoke", turn=1)["stored"] is True
    assert "results" in tools.memory_search("ping", session="smoke")
    assert "summary" in tools.memory_summarize(session="smoke")
    assert "total_tokens" in tools.memory_stats()
