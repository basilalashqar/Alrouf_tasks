"""
Embedding service for RAG Knowledge Base
"""

import json
import logging
import numpy as np
from typing import List, Dict, Optional, Any
from datetime import datetime

try:
    import openai
except ImportError:
    openai = None

from config import Config

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        self.config = Config()
        self.client = None
        
        if not self.config.use_mock_services and not self.config.mock_openai and self.config.openai_api_key:
            try:
                self.client = openai.OpenAI(api_key=self.config.openai_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def generate_embeddings(self, documents: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for a list of documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of documents with embeddings
        """
        try:
            logger.info(f"Generating embeddings for {len(documents)} documents")
            
            if self.client and not self.config.use_mock_services:
                return self._generate_with_openai(documents)
            else:
                return self._generate_mock_embeddings(documents)
                
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return documents  # Return original documents if embedding fails
    
    def _generate_with_openai(self, documents: List[Dict]) -> List[Dict]:
        """Generate embeddings using OpenAI API"""
        try:
            # Extract texts for embedding
            texts = [doc["content"] for doc in documents]
            
            # Generate embeddings in batches
            embeddings = []
            for i in range(0, len(texts), self.config.batch_size):
                batch_texts = texts[i:i + self.config.batch_size]
                
                response = self.client.embeddings.create(
                    model=self.config.embedding_model,
                    input=batch_texts
                )
                
                batch_embeddings = [data.embedding for data in response.data]
                embeddings.extend(batch_embeddings)
                
                logger.info(f"Generated embeddings for batch {i//self.config.batch_size + 1}")
            
            # Add embeddings to documents
            for i, doc in enumerate(documents):
                doc["embedding"] = embeddings[i]
                doc["metadata"]["embedding_model"] = self.config.embedding_model
                doc["metadata"]["embedding_generated_at"] = datetime.now().isoformat()
            
            logger.info(f"Successfully generated {len(embeddings)} embeddings")
            return documents
            
        except Exception as e:
            logger.error(f"OpenAI embedding generation failed: {e}")
            return self._generate_mock_embeddings(documents)
    
    def _generate_mock_embeddings(self, documents: List[Dict]) -> List[Dict]:
        """Generate mock embeddings for testing"""
        try:
            import random
            import hashlib
            
            for doc in documents:
                # Generate deterministic mock embedding based on content
                content_hash = hashlib.md5(doc["content"].encode()).hexdigest()
                random.seed(int(content_hash[:8], 16))  # Use hash as seed
                
                # Generate random embedding vector
                embedding = [random.random() for _ in range(1536)]  # OpenAI embedding size
                
                doc["embedding"] = embedding
                doc["metadata"]["embedding_model"] = "mock-embedding-model"
                doc["metadata"]["embedding_generated_at"] = datetime.now().isoformat()
                doc["metadata"]["mock_embedding"] = True
            
            logger.info(f"Generated {len(documents)} mock embeddings")
            return documents
            
        except Exception as e:
            logger.error(f"Error generating mock embeddings: {e}")
            return documents
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query
        
        Args:
            query: Query string
            
        Returns:
            Query embedding vector
        """
        try:
            if self.client and not self.config.use_mock_services:
                return self._generate_query_embedding_with_openai(query)
            else:
                return self._generate_mock_query_embedding(query)
                
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            return self._generate_mock_query_embedding(query)
    
    def _generate_query_embedding_with_openai(self, query: str) -> List[float]:
        """Generate query embedding using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=self.config.embedding_model,
                input=query
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"OpenAI query embedding failed: {e}")
            return self._generate_mock_query_embedding(query)
    
    def _generate_mock_query_embedding(self, query: str) -> List[float]:
        """Generate mock query embedding"""
        try:
            import random
            import hashlib
            
            # Generate deterministic mock embedding
            query_hash = hashlib.md5(query.encode()).hexdigest()
            random.seed(int(query_hash[:8], 16))
            
            return [random.random() for _ in range(1536)]
            
        except Exception as e:
            logger.error(f"Error generating mock query embedding: {e}")
            return [0.0] * 1536  # Return zero vector as fallback
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            if self.client and not self.config.use_mock_services:
                return self._batch_embeddings_with_openai(texts)
            else:
                return self._batch_mock_embeddings(texts)
                
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return self._batch_mock_embeddings(texts)
    
    def _batch_embeddings_with_openai(self, texts: List[str]) -> List[List[float]]:
        """Generate batch embeddings using OpenAI"""
        try:
            embeddings = []
            
            for i in range(0, len(texts), self.config.batch_size):
                batch_texts = texts[i:i + self.config.batch_size]
                
                response = self.client.embeddings.create(
                    model=self.config.embedding_model,
                    input=batch_texts
                )
                
                batch_embeddings = [data.embedding for data in response.data]
                embeddings.extend(batch_embeddings)
            
            return embeddings
            
        except Exception as e:
            logger.error(f"OpenAI batch embedding failed: {e}")
            return self._batch_mock_embeddings(texts)
    
    def _batch_mock_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock batch embeddings"""
        try:
            import random
            import hashlib
            
            embeddings = []
            for text in texts:
                # Generate deterministic mock embedding
                text_hash = hashlib.md5(text.encode()).hexdigest()
                random.seed(int(text_hash[:8], 16))
                
                embedding = [random.random() for _ in range(1536)]
                embeddings.append(embedding)
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating mock batch embeddings: {e}")
            return [[0.0] * 1536 for _ in texts]
    
    def get_embedding_stats(self) -> Dict:
        """Get embedding service statistics"""
        try:
            stats = {
                "service_type": "OpenAI" if self.client else "Mock",
                "model": self.config.embedding_model,
                "embedding_dimension": 1536,
                "batch_size": self.config.batch_size,
                "status": "healthy"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting embedding stats: {e}")
            return {"status": "error", "message": str(e)}
