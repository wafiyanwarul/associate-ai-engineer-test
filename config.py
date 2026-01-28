"""
Configuration Management Module

Centralizes all application settings with environment variable support.
This eliminates hardcoded values and makes the application more flexible.
"""

import os
from typing import Optional


class Config:
    """Application configuration with sensible defaults."""
    
    # Qdrant Configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "demo_collection")
    
    # Embedding Configuration
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "128"))
    
    # API Configuration
    API_TITLE: str = "Learning RAG Demo"
    API_VERSION: str = "1.0.0"
    
    # Search Configuration
    SEARCH_LIMIT: int = int(os.getenv("SEARCH_LIMIT", "2"))
    ANSWER_PREVIEW_LENGTH: int = 100  # Characters to show in answer preview
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values.
        
        Returns:
            bool: True if config is valid, raises ValueError otherwise
        """
        if cls.EMBEDDING_DIMENSION <= 0:
            raise ValueError("EMBEDDING_DIMENSION must be positive")
        
        if cls.SEARCH_LIMIT <= 0:
            raise ValueError("SEARCH_LIMIT must be positive")
        
        return True


# Validate config on module import
Config.validate()