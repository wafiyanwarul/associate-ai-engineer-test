"""
Embedding Service

Handles text-to-vector conversion. Currently uses a deterministic
fake embedding for demo purposes, but designed to be easily swapped
with real models (OpenAI, HuggingFace, etc.)
"""

import random
from typing import List
from config import Config


class EmbeddingService:
    """
    Service untuk generate embeddings dari text.
    
    Design note: Interface ini bikin gampang nanti kalo mau ganti
    dari fake embedding ke real model (e.g., sentence-transformers).
    """
    
    def __init__(self, dimension: int = None):
        """
        Initialize embedding service.
        
        Args:
            dimension: Vector dimension. Defaults to config value.
        """
        self.dimension = dimension or Config.EMBEDDING_DIMENSION
    
    def embed(self, text: str) -> List[float]:
        """
        Convert text to embedding vector.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Note:
            Currently uses deterministic random for demo.
            Seed based on text hash ensures same text = same vector.
        """
        # Seed berdasarkan hash text biar deterministic
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.dimension)]
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts at once.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
            
        Note:
            Useful untuk batch processing documents.
        """
        return [self.embed(text) for text in texts]