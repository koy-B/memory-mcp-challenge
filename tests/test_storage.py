"""Tests stockage — recherche sémantique réelle requise."""

from memory_mcp.storage import MemoryStore
from memory_mcp.validation import top1_contains


def test_store_and_search_paraphrase():
    """Le bag-of-words naïf échoue sur cette paraphrase."""
    store = MemoryStore()
    store.store(
        "La cliente s'appelle Marie Dupont, statut premium",
        tags=["client"],
        session="s1",
        turn=1,
    )
    store.store("Référence dossier CTR-2024-8847", tags=["contrat"], session="s1", turn=3)
    store.store("Bruit: recette gâteau chocolat sans lactose", session="s1", turn=99)

    hits = store.search("identité de l'interlocutrice", top_k=1, session="s1")
    results = [{"content": h.content} for h in hits]
    assert top1_contains("Marie Dupont", results)


def test_list_session_ordered():
    store = MemoryStore()
    store.store("tour 1", session="s2", turn=1)
    store.store("tour 3", session="s2", turn=3)
    store.store("tour 2", session="s2", turn=2)

    entries = store.list_session("s2")
    assert [e.turn for e in entries] == [1, 2, 3]


def test_count():
    store = MemoryStore()
    assert store.count() == 0
    store.store("a")
    store.store("b")
    assert store.count() == 2
