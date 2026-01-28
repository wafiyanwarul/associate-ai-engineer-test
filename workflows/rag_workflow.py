"""
RAG Workflow

Orchestrates the retrieval-augmented generation flow:
1. Retrieve relevant documents based on query
2. Generate answer from retrieved context

This workflow uses LangGraph for state management but keeps
the business logic simple and testable.
"""

from typing import Dict, List, Any
from langgraph.graph import StateGraph, END
from services import EmbeddingService, DocumentStore
from config import Config


class RagWorkflow:
    """
    Manages the RAG (Retrieval-Augmented Generation) workflow.

    Design note: This class orchestrates services but doesn't contain
    business logic itself - that's in the services layer.
    """

    def __init__(
        self, embedding_service: EmbeddingService, document_store: DocumentStore
    ):
        """
        Initialize RAG workflow with required services.

        Args:
            embedding_service: Service for text embeddings
            document_store: Service for document storage/retrieval
        """
        self.embedding_service = embedding_service
        self.document_store = document_store
        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        """
        Build LangGraph workflow.

        Returns:
            Compiled workflow graph
        """
        workflow = StateGraph(dict)

        # Add nodes dengan bound methods
        workflow.add_node("retrieve", self._retrieve_step)
        workflow.add_node("answer", self._answer_step)

        # Define flow
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "answer")
        workflow.add_edge("answer", END)

        return workflow.compile()

    def _retrieve_step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 1: Retrieve relevant documents.

        Args:
            state: Current workflow state containing 'question'

        Returns:
            Updated state with 'context' field
        """
        question = state.get("question", "")

        # Generate query embedding
        query_embedding = self.embedding_service.embed(question)

        # Search for relevant docs
        results = self.document_store.search(
            query_embedding=query_embedding, limit=Config.SEARCH_LIMIT
        )

        state["context"] = results
        return state

    def _answer_step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Generate answer from context.

        Args:
            state: Current workflow state containing 'context'

        Returns:
            Updated state with 'answer' field
        """
        context = state.get("context", [])

        if context:
            # Ambil context pertama dan preview
            preview_length = Config.ANSWER_PREVIEW_LENGTH
            first_context = context[0]

            # Truncate kalo kepanjangan
            preview = first_context[:preview_length]
            if len(first_context) > preview_length:
                preview += "..."

            answer = f"I found this: '{preview}'"
        else:
            answer = "Sorry, I don't know."

        state["answer"] = answer
        return state

    def run(self, question: str) -> Dict[str, Any]:
        """
        Execute the RAG workflow.

        Args:
            question: User question

        Returns:
            Dict containing answer and context used
        """
        initial_state = {"question": question}
        result = self.graph.invoke(initial_state)
        return result

    def add_document(self, text: str, doc_id: int = None) -> bool:
        """
        Add document to knowledge base.

        Args:
            text: Document text
            doc_id: Optional document ID (auto-generated if None)

        Returns:
            True if successful

        Note:
            This is a convenience method. The actual storage
            logic is in DocumentStore.
        """
        # Auto-generate ID if not provided
        if doc_id is None:
            stats = self.document_store.get_stats()
            doc_id = stats["in_memory_count"]

        # Generate embedding
        embedding = self.embedding_service.embed(text)

        # Store document
        return self.document_store.add_document(
            doc_id=doc_id, text=text, embedding=embedding
        )
