"""
Services Package

Contains business logic components that can be used independently.
Each service focuses on a single responsibility.
- EmbeddingService: Text to vector conversion
- DocumentStore: Document storage and retrieval
"""
from .embedding_service import EmbeddingService
from .document_store import DocumentStore

__all__ = ["EmbeddingService", "DocumentStore"]