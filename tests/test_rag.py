from app.services.rag import RAGService


def test_annual_leave_policy():
    rag = RAGService()

    result = rag.answer(
        "How many annual leave days do employees receive?",
        top_k=3,
    )

    assert result["retrieval_count"] > 0
    assert len(result["sources"]) > 0
    assert "18" in result["answer"]


def test_long_leave_policy():
    rag = RAGService()

    result = rag.answer(
        "How far in advance should long leave requests be submitted?",
        top_k=3,
    )

    assert result["retrieval_count"] > 0
    assert len(result["sources"]) > 0


def test_security_policy():
    rag = RAGService()

    result = rag.answer(
        "What should an employee do after detecting a security incident?",
        top_k=3,
    )

    assert result["retrieval_count"] > 0
    assert len(result["sources"]) > 0
    assert "security" in result["answer"].lower()


def test_unknown_policy_question():
    rag = RAGService()

    result = rag.answer(
        "What is the company's policy for purchasing a private jet?",
        top_k=3,
    )

    assert result["answer"]