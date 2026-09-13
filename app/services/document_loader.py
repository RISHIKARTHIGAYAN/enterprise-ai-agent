from pathlib import Path

from pypdf import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n".join(pages)


def load_docx(path: Path) -> str:
    document = Document(str(path))

    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def load_document(path: Path) -> str:

    suffix = path.suffix.lower()

    if suffix == ".txt":
        return load_txt(path)

    if suffix == ".pdf":
        return load_pdf(path)

    if suffix == ".docx":
        return load_docx(path)

    raise ValueError(
        f"Unsupported document type: {suffix}"
    )


def load_documents(directory: str):

    directory_path = Path(directory)

    documents = []

    for path in directory_path.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = load_document(path)

        if not text.strip():
            continue

        documents.append(
            {
                "source": path.name,
                "path": str(path),
                "text": text,
            }
        )

    return documents