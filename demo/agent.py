"""Agent de démo — stub à compléter par les équipes du hackathon."""

from __future__ import annotations

import json
from pathlib import Path

from memory_mcp.tools import MemoryTools

ROOT = Path(__file__).parent.parent
CONVERSATION = ROOT / "benchmark" / "conversation.json"


def run_demo(session: str = "demo") -> None:
    """Joue une conversation de démo avec le serveur mémoire."""
    tools = MemoryTools()
    turns = json.loads(CONVERSATION.read_text(encoding="utf-8"))

    print(f"=== Démo agent mémoire (session: {session}) ===\n")
    for turn in turns:
        tools.memory_store(
            content=f"{turn['role']}: {turn['content']}",
            tags=[turn["role"]],
            session=session,
            turn=turn["turn"],
        )
        print(f"Tour {turn['turn']} — stocké")

    summary = tools.memory_summarize(session=session)
    stats = tools.memory_stats()
    print(f"\nRésumé : {summary['summary'][:200]}...")
    print(f"Stats : {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    run_demo()
