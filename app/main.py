from pathlib import Path
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.agent.graph import EnterpriseAgentGraph
from app.services.upload_service import DocumentUploadService


app = FastAPI(
    title="Enterprise AI Agent",
    description="Local-first enterprise AI agent with RAG, SQL, calculator tools, guardrails, and LangGraph orchestration.",
    version="1.0.0",
)


agent = EnterpriseAgentGraph()
upload_service = DocumentUploadService()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = PROJECT_ROOT / "app" / "templates" / "index.html"


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    route: str | None
    answer: str | None
    sources: list
    error: str | None


@app.get("/")
def home():
    return FileResponse(INDEX_FILE)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "enterprise-ai-agent",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = agent.run(request.question)

    return {
        "question": request.question,
        "route": result.get("route"),
        "answer": result.get("answer"),
        "sources": result.get("sources", []),
        "error": result.get("error"),
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in {".txt", ".pdf", ".docx"}:
        return {
            "success": False,
            "error": "Unsupported file type. Only TXT, PDF, and DOCX files are allowed.",
        }

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temporary_file:

            contents = await file.read()
            temporary_file.write(contents)
            temporary_path = temporary_file.name

        result = upload_service.upload(
            temporary_path,
            file.filename,
        )

        Path(temporary_path).unlink(missing_ok=True)

        return {
            "success": True,
            "filename": result["filename"],
            "chunks_indexed": result["chunks_indexed"],
        }

    except Exception as error:

        Path(temporary_path).unlink(missing_ok=True)

        return {
            "success": False,
            "error": str(error),
        }