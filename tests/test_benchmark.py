from benchmark.harness import (
    CONVERSATION_PATH,
    evaluate_trap_questions,
    generate_long_conversation,
    load_json,
    run_benchmark,
    simulate_memory_conversation,
)
from benchmark.naive import simulate_naive_conversation
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools

SAMPLE_TURNS = [
    {"turn": 1, "role": "user", "content": "Je suis Marie Dupont."},
    {"turn": 2, "role": "assistant", "content": "Bonjour Marie."},
    {"turn": 3, "role": "user", "content": "Mon contrat est CTR-2024-8847."},
]


def test_naive_grows_tokens():
    result = simulate_naive_conversation(SAMPLE_TURNS)
    assert result["mode"] == "naive"
    assert result["total_tokens"] > 0
    # Le mode naïf re-envoie tout l'historique : coût cumulé > dernier tour seul
    assert result["total_tokens"] > result["tokens_per_turn"][-1]


def test_memory_uses_fewer_tokens_than_naive():
    """Sur 40 tours, le contexte compressé doit coûter moins que l'historique complet."""
    base = load_json(CONVERSATION_PATH)
    turns = generate_long_conversation(base, target_turns=40)
    naive = simulate_naive_conversation(turns)
    memory = simulate_memory_conversation(turns, session="bench-full")
    assert memory["total_tokens"] < naive["total_tokens"]


def test_benchmark_report_structure():
    report = run_benchmark()
    assert "naive" in report
    assert "memory" in report
    assert "savings_pct" in report
    assert "quality" in report
    assert report["savings_pct"] >= 0


def test_trap_questions_marie():
    reset_stats()
    tools = MemoryTools()
    tools.memory_store(
        "user: Bonjour, je suis Marie Dupont, cliente premium.", session="benchmark", turn=1
    )
    tools.memory_store(
        "user: Mon numéro de contrat est CTR-2024-8847.", session="benchmark", turn=3
    )
    tools.memory_store("user: Mon email est marie.dupont@email.fr.", session="benchmark", turn=9)

    quality = evaluate_trap_questions(tools, session="benchmark")
    assert quality["passed"] >= 2
