from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_DIRECTORY = PROJECT_ROOT / "data" / "documents"

CHROMA_DIRECTORY = PROJECT_ROOT / "data" / "chroma"

CHROMA_COLLECTION = "enterprise_documents"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LLM_MODEL = "llama3.2:3b"

TOP_K = 5