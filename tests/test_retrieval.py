from app.services.vector_store import VectorStore


def test_retrieval_returns_results():
    vector_store = VectorStore()

    results = vector_store.search(
        "annual leave policy",
        top_k=3,
    )

    assert isinstance(results, list)
    assert len(results) > 0


def test_retrieval_contains_source_metadata():
    vector_store = VectorStore()

    results = vector_store.search(
        "security incident",
        top_k=3,
    )

    assert len(results) > 0

    for result in results:
        assert "text" in result
        assert "source" in result
        assert "distance" in result