"""
Vector database integration using Pinecone
"""

from typing import List, Dict, Optional
from pinecone import Pinecone, ServerlessSpec
from config import settings
import time


class VectorStore:
    """Pinecone vector store for document embeddings"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        self.index = None
        self._ensure_index_exists()
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            
            if self.index_name not in existing_indexes:
                print(f"Creating Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=settings.embedding_dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                # Wait for index to be ready
                time.sleep(1)
            
            self.index = self.pc.Index(self.index_name)
            print(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            print(f"Error setting up Pinecone: {e}")
            raise
    
    def upsert_chunks(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]],
        document_name: str
    ) -> int:
        """
        Store document chunks with embeddings in Pinecone
        
        Args:
            chunks: List of chunk dictionaries
            embeddings: List of embedding vectors
            document_name: Name of the source document
        
        Returns:
            Number of chunks stored
        """
        vectors = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{document_name}_{chunk['chunk_index']}"
            
            vectors.append({
                'id': vector_id,
                'values': embedding,
                'metadata': {
                    'document_name': document_name,
                    'content': chunk['content'],
                    'word_count': chunk['word_count'],
                    'chunk_index': chunk['chunk_index']
                }
            })
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            self.index.upsert(vectors=batch)
        
        return len(vectors)
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar chunks
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_dict: Optional metadata filters
        
        Returns:
            List of matching chunks with scores
        """
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        chunks = []
        for match in results['matches']:
            chunks.append({
                'id': match['id'],
                'score': match['score'],
                'document_name': match['metadata']['document_name'],
                'content': match['metadata']['content'],
                'word_count': match['metadata']['word_count'],
                'chunk_index': match['metadata']['chunk_index']
            })
        
        return chunks
    
    def delete_document(self, document_name: str) -> bool:
        """Delete all chunks for a document"""
        try:
            self.index.delete(filter={'document_name': document_name})
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get index statistics"""
        return self.index.describe_index_stats()


# Global vector store instance
vector_store = VectorStore()
