"""
API Request/Response Models

Defines Pydantic schemas for data validation and serialization.
Separates API contracts from business logic.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class QuestionRequest(BaseModel):
    """Request schema for asking questions."""
    
    question: str = Field(
        ..., 
        min_length=1,
        description="User question to be answered by the RAG system"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is LangGraph?"
            }
        }


class DocumentRequest(BaseModel):
    """Request schema for adding documents."""
    
    text: str = Field(
        ...,
        min_length=1,
        description="Document text to be added to knowledge base"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "LangGraph is a library for building stateful workflows."
            }
        }


class QuestionResponse(BaseModel):
    """Response schema for question answering."""
    
    question: str = Field(..., description="Original question")
    answer: str = Field(..., description="Generated answer")
    context_used: List[str] = Field(..., description="Retrieved context documents")
    latency_sec: float = Field(..., description="Processing time in seconds")


class DocumentResponse(BaseModel):
    """Response schema for document addition."""
    
    id: int = Field(..., description="Document ID")
    status: str = Field(..., description="Operation status")


class StatusResponse(BaseModel):
    """Response schema for system status."""
    
    qdrant_ready: bool = Field(..., description="Whether Qdrant is available")
    storage_type: str = Field(..., description="Current storage backend")
    document_count: int = Field(..., description="Number of documents stored")
    graph_ready: bool = Field(..., description="Whether RAG workflow is ready")