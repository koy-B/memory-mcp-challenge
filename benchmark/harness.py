"""Harnais de benchmark : compare mode naïf vs serveur mémoire MCP."""

from __future__ import annotations

import json
from pathlib import Path

from benchmark.naive import simulate_naive_conversation
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools

ROOT = Path(__file__).parent
CONVERSATION_PATH = ROOT / "conversation.json"
TRAP_PATH = ROOT / "trap_questions.json"


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text(encoding="utf-8"))


def generate_long_conversation(base_turns: list[dict], target_turns: int = 40) -> list[dict]:
    """Étend une conversation courte en alternant rôles jusqu'à target_turns."""
    turns = list(base_turns)
    turn_num = len(turns) + 1
    roles = ("user", "assistant")
    while len(turns) < target_turns:
        role = roles[(turn_num - 1) % 2]
        turns.append(
            {
                "turn": turn_num,
                "role": role,
                "content": f"Échange {turn_num} — précision contextuelle pour le tour {turn_num}.",
            }
        )
        turn_num += 1
    return turns


def _context_tokens(tools: MemoryTools, session: str, query: str) -> int:
    """Tokens réellement envoyés au LLM : résumé + résultats de recherche."""
    from memory_mcp.stats import count_tokens

    summary = tools.memory_summarize(session=session)
    search = tools.memory_search(query=query, top_k=3, session=session)
    context = summary["summary"] + "\n" + "\n".join(r["content"] for r in search["results"])
    return count_tokens(context)


def simulate_memory_conversation(turns: list[dict], session: str = "benchmark") -> dict:
    """Simule une conversation avec le serveur mémoire."""
    reset_stats()
    tools = MemoryTools()
    total_context_tokens = 0

    for turn in turns:
        role = turn["role"]
        content = turn["content"]
        tools.memory_store(
            content=f"{role}: {content}",
            tags=[role, f"turn-{turn['turn']}"],
            session=session,
            turn=turn["turn"],
        )
        # Seul le contexte récupéré (résumé + search) part vers le LLM
        total_context_tokens += _context_tokens(tools, session, content)

    stats = tools.memory_stats()
    return {
        "mode": "memory",
        "turns": len(turns),
        "total_tokens": total_context_tokens,
        "stats": stats,
    }


def evaluate_trap_questions(tools: MemoryTools, session: str = "benchmark") -> dict:
    """Évalue les questions pièges (axe qualité)."""
    traps = load_json(TRAP_PATH)
    passed = 0
    details = []

    for trap in traps:
        result = tools.memory_search(query=trap["question"], top_k=3, session=session)
        contents = " ".join(r["content"] for r in result["results"])
        ok = trap["expected"].lower() in contents.lower()
        if ok:
            passed += 1
        details.append({"question": trap["question"], "expected": trap["expected"], "passed": ok})

    return {
        "total": len(traps),
        "passed": passed,
        "score_pct": round(100 * passed / len(traps), 1) if traps else 0.0,
        "details": details,
    }


def run_benchmark(turn_count: int = 40) -> dict:
    """Lance le benchmark complet et retourne le rapport."""
    base = load_json(CONVERSATION_PATH)
    turns = generate_long_conversation(base, target_turns=turn_count)
    naive = simulate_naive_conversation(turns)
    memory = simulate_memory_conversation(turns)

    reset_stats()
    tools = MemoryTools()
    for turn in turns:
        tools.memory_store(
            content=f"{turn['role']}: {turn['content']}",
            tags=[turn["role"]],
            session="benchmark",
            turn=turn["turn"],
        )
    quality = evaluate_trap_questions(tools, session="benchmark")

    savings_pct = 0.0
    if naive["total_tokens"] > 0:
        savings_pct = round(100 * (1 - memory["total_tokens"] / naive["total_tokens"]), 1)

    return {
        "naive": naive,
        "memory": memory,
        "savings_pct": savings_pct,
        "quality": quality,
    }


def main() -> None:
    report = run_benchmark()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
