from pathlib import Path
import shutil

from app.config import DOCUMENT_DIRECTORY
from app.services.document_loader import load_document
from app.services.vector_store import VectorStore


ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
}


class DocumentUploadService:

    def __init__(self):
        DOCUMENT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.vector_store = VectorStore()

    def upload(self, file_path: str, filename: str):
        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "Unsupported file type. "
                "Only TXT, PDF, and DOCX files are allowed."
            )

        destination = DOCUMENT_DIRECTORY / Path(filename).name

        shutil.copy2(
            file_path,
            destination,
        )

        text = load_document(destination)

        if not text.strip():
            destination.unlink(missing_ok=True)

            raise ValueError(
                "The uploaded document contains no readable text."
            )

        document = {
            "source": destination.name,
            "path": str(destination),
            "text": text,
        }

        chunk_count = self.vector_store.ingest(
            [document]
        )

        return {
            "filename": destination.name,
            "chunks_indexed": chunk_count,
        }