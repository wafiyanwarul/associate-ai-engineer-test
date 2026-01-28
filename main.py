"""
Learning RAG Demo - Main Application

Entry point for the RAG (Retrieval-Augmented Generation) service.
Initializes components and wires up dependencies.
"""

from fastapi import FastAPI
from config import Config
from services import EmbeddingService, DocumentStore
from workflows import RagWorkflow
from api import RagAPI
from api.models import (
    QuestionRequest,
    QuestionResponse,
    DocumentRequest,
    DocumentResponse,
    StatusResponse
)

# Initialize FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    version=Config.API_VERSION,
    description="A simple RAG service demonstrating clean architecture principles"
)

# Initialize services (dependency injection)
embedding_service = EmbeddingService()
document_store = DocumentStore()

# Initialize workflow with services
rag_workflow = RagWorkflow(
    embedding_service=embedding_service,
    document_store=document_store
)

# Initialize API handler
api = RagAPI(workflow=rag_workflow)


# === ENDPOINTS ===

@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    """
    Answer a question using RAG.
    
    Retrieves relevant context from the knowledge base and generates an answer.
    """
    return api.ask_question(request)


@app.post("/add", response_model=DocumentResponse)
def add_document(request: DocumentRequest) -> DocumentResponse:
    """
    Add a document to the knowledge base.
    
    The document will be embedded and stored for future retrieval.
    """
    return api.add_document(request)


@app.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """
    Get system status.
    
    Returns information about storage backend and system readiness.
    """
    return api.get_status()


# Optional: Add root endpoint for health check
@app.get("/")
def root():
    """Root endpoint - health check."""
    return {
        "status": "running",
        "message": "Learning RAG Demo API",
        "docs": "/docs"
    }