"""
Document Store Service

Manages document storage and retrieval using Qdrant vector database
with in-memory fallback. Handles connection failures gracefully.
"""

from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from config import Config


class DocumentStore:
    """
    Handles document storage with Qdrant + in-memory fallback.
    
    Design decisions:
    - Graceful degradation: kalo Qdrant fail, pake in-memory
    - Encapsulates storage logic: API layer ga perlu tau detail storage
    - Single responsibility: cuma ngurus storage, bukan business logic
    """
    
    def __init__(self, qdrant_url: str = None, collection_name: str = None):
        """
        Initialize document store.
        
        Args:
            qdrant_url: Qdrant server URL
            collection_name: Collection name in Qdrant
        """
        self.qdrant_url = qdrant_url or Config.QDRANT_URL
        self.collection_name = collection_name or Config.QDRANT_COLLECTION
        self.using_qdrant = False
        self.memory_store: List[Dict] = []  # Fallback storage
        
        # Try connect to Qdrant
        self._initialize_qdrant()
    
    def _initialize_qdrant(self) -> None:
        """
        Setup Qdrant connection and collection.
        Falls back to in-memory if connection fails.
        """
        try:
            self.client = QdrantClient(self.qdrant_url)
            
            # Recreate collection (fresh start tiap run)
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=Config.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE
                )
            )
            
            self.using_qdrant = True
            print(f"✅ Qdrant connected at {self.qdrant_url}")
            
        except Exception as e:
            print(f"⚠️  Qdrant not available: {e}")
            print("📝 Using in-memory storage as fallback")
            self.using_qdrant = False
    
    def add_document(self, doc_id: int, text: str, embedding: List[float]) -> bool:
        """
        Add document to storage.
        
        Args:
            doc_id: Unique document ID
            text: Document text content
            embedding: Vector embedding of the text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.using_qdrant:
                point = PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={"text": text}
                )
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[point]
                )
            else:
                # Fallback: store in memory
                self.memory_store.append({
                    "id": doc_id,
                    "text": text,
                    "embedding": embedding
                })
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding document: {e}")
            return False
    
    def search(self, query_embedding: List[float], limit: int = None) -> List[str]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query vector
            limit: Max results to return
            
        Returns:
            List of matching document texts
        """
        limit = limit or Config.SEARCH_LIMIT
        results = []
        
        try:
            if self.using_qdrant:
                # Vector search pake Qdrant
                hits = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=limit
                )
                results = [hit.payload["text"] for hit in hits]
                
            else:
                # Fallback: simple text matching (ga pake similarity score)
                # Note: ini simple banget, real case harusnya pake cosine similarity
                for doc in self.memory_store[:limit]:
                    results.append(doc["text"])
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """
        Get storage statistics.
        
        Returns:
            Dict containing storage info
        """
        return {
            "using_qdrant": self.using_qdrant,
            "qdrant_url": self.qdrant_url if self.using_qdrant else None,
            "collection_name": self.collection_name if self.using_qdrant else None,
            "in_memory_count": len(self.memory_store)
        }