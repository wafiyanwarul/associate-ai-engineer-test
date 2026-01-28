"""
API Routes

Defines FastAPI endpoints for the RAG service.
Handles HTTP requests/responses and delegates work to workflow layer.
"""

import time
from fastapi import HTTPException
from typing import Dict, Any

from .models import (
    QuestionRequest, 
    QuestionResponse,
    DocumentRequest, 
    DocumentResponse,
    StatusResponse
)
from workflows import RagWorkflow


class RagAPI:
    """
    API handler for RAG endpoints.
    
    Design note: This class acts as a thin controller layer,
    delegating actual work to the workflow layer.
    """
    
    def __init__(self, workflow: RagWorkflow):
        """
        Initialize API with RAG workflow.
        
        Args:
            workflow: RagWorkflow instance for handling requests
        """
        self.workflow = workflow
    
    def ask_question(self, request: QuestionRequest) -> QuestionResponse:
        """
        Handle question answering requests.
        
        Args:
            request: Question request with user query
            
        Returns:
            QuestionResponse with answer and metadata
            
        Raises:
            HTTPException: If processing fails
        """
        start_time = time.time()
        
        try:
            # Delegate to workflow
            result = self.workflow.run(request.question)
            
            # Calculate latency
            latency = round(time.time() - start_time, 3)
            
            return QuestionResponse(
                question=request.question,
                answer=result["answer"],
                context_used=result.get("context", []),
                latency_sec=latency
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error processing question: {str(e)}"
            )
    
    def add_document(self, request: DocumentRequest) -> DocumentResponse:
        """
        Handle document addition requests.
        
        Args:
            request: Document request with text content
            
        Returns:
            DocumentResponse with document ID and status
            
        Raises:
            HTTPException: If addition fails
        """
        try:
            # Get current doc count for ID
            stats = self.workflow.document_store.get_stats()
            doc_id = stats["in_memory_count"]
            
            # Add document via workflow
            success = self.workflow.add_document(
                text=request.text,
                doc_id=doc_id
            )
            
            if not success:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to add document"
                )
            
            return DocumentResponse(
                id=doc_id,
                status="added"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error adding document: {str(e)}"
            )
    
    def get_status(self) -> StatusResponse:
        """
        Get system status.
        
        Returns:
            StatusResponse with system information
        """
        stats = self.workflow.document_store.get_stats()
        
        # Determine storage type
        storage_type = "qdrant" if stats["using_qdrant"] else "in-memory"
        
        return StatusResponse(
            qdrant_ready=stats["using_qdrant"],
            storage_type=storage_type,
            document_count=stats["in_memory_count"],
            graph_ready=self.workflow.graph is not None
        )