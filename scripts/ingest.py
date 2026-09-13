from app.config import DOCUMENT_DIRECTORY
from app.services.document_loader import load_documents
from app.services.vector_store import VectorStore


def main():

    print("Loading documents...")

    documents = load_documents(
        str(DOCUMENT_DIRECTORY)
    )

    print(
        f"Loaded {len(documents)} documents."
    )

    if not documents:

        print(
            "No documents found."
        )

        return

    store = VectorStore()

    count = store.ingest(
        documents
    )

    print(
        f"Indexed {count} document chunks."
    )


if __name__ == "__main__":
    main()