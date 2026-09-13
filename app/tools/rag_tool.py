from app.services.rag import RAGService


class RAGTool:

    def __init__(self):
        self.rag = RAGService()

    def run(self, question: str):

        result = self.rag.answer(
            question,
            top_k=3,
        )

        return {
            "tool": "rag",
            "answer": result["answer"],
            "sources": result["sources"],
            "retrieval_count": result["retrieval_count"],
        }