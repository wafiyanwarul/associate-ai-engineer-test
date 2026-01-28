"""
API Package

Contains HTTP layer components:
- models: Pydantic schemas for request/response validation
- routes: FastAPI endpoint handlers

This layer handles HTTP concerns and delegates work to the workflow layer.
"""

from .models import (
    QuestionRequest,
    QuestionResponse,
    DocumentRequest,
    DocumentResponse,
    StatusResponse
)
from .routes import RagAPI

__all__ = [
    "QuestionRequest",
    "QuestionResponse", 
    "DocumentRequest",
    "DocumentResponse",
    "StatusResponse",
    "RagAPI"
]