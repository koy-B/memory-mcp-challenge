from memory_mcp.storage import MemoryStore


def test_store_and_search():
    store = MemoryStore()
    store.store("Marie Dupont est cliente premium", tags=["client"], session="s1", turn=1)
    store.store("Contrat CTR-2024-8847", tags=["contrat"], session="s1", turn=3)

    hits = store.search("nom du client", top_k=2, session="s1")
    assert len(hits) >= 1
    assert "Marie" in hits[0].content


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
