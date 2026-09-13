from app.services.vector_store import VectorStore
from app.services.llm import generate_answer


class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()

    def answer(self, question: str, top_k: int = 5):
        results = self.vector_store.search(question, top_k=top_k)

        if not results:
            return {
                "answer": "I could not find relevant information in the knowledge base.",
                "sources": [],
                "retrieval_count": 0,
            }

        # ChromaDB distance: lower = more relevant.
        # Keep only reasonably relevant results.
        RELEVANCE_THRESHOLD = 1.1

        relevant_results = [
            result
            for result in results
            if result["distance"] <= RELEVANCE_THRESHOLD
        ]

        if not relevant_results:
            return {
                "answer": "I could not find relevant information in the knowledge base.",
                "sources": [],
                "retrieval_count": 0,
            }

        context_parts = []
        sources = []

        for result in relevant_results:
            context_parts.append(
                f"[Source: {result['source']}]\n{result['text']}"
            )

            sources.append({
                "source": result["source"],
                "distance": result["distance"],
            })

        context = "\n\n".join(context_parts)

        answer = generate_answer(
            question,
            context,
        )

        return {
            "answer": answer,
            "sources": sources,
            "retrieval_count": len(relevant_results),
        }