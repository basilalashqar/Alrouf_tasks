"""
Vector store implementation for RAG Knowledge Base
"""

import json
import logging
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime

try:
    import faiss
    import numpy as np
except ImportError:
    faiss = None
    np = None

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None

from config import Config

logger = logging.getLogger(__name__)

class VectorStore:
    """Vector store for storing and retrieving embeddings"""
    
    def __init__(self):
        self.config = Config()
        self.index = None
        self.metadata = []
        self.embeddings = []
        self.chroma_client = None
        self.chroma_collection = None
        
        # Initialize based on configuration
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize the vector store"""
        try:
            if self.config.vector_db_type == "faiss":
                self._initialize_faiss()
            elif self.config.vector_db_type == "chroma":
                self._initialize_chroma()
            else:
                logger.warning(f"Unsupported vector DB type: {self.config.vector_db_type}")
                self._initialize_mock()
            
            logger.info(f"Vector store initialized with {self.config.vector_db_type}")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            self._initialize_mock()
    
    def _initialize_faiss(self):
        """Initialize FAISS index"""
        try:
            if not faiss or not np:
                logger.warning("FAISS not available, using mock store")
                self._initialize_mock()
                return
            
            # Create or load FAISS index
            index_path = Path(self.config.faiss_index_path)
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            if index_path.exists():
                # Load existing index
                self.index = faiss.read_index(str(index_path))
                self._load_metadata()
                logger.info(f"Loaded existing FAISS index with {self.index.ntotal} vectors")
            else:
                # Create new index
                dimension = 1536  # OpenAI embedding dimension
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                logger.info("Created new FAISS index")
            
        except Exception as e:
            logger.error(f"Error initializing FAISS: {e}")
            self._initialize_mock()
    
    def _initialize_chroma(self):
        """Initialize ChromaDB"""
        try:
            if not chromadb:
                logger.warning("ChromaDB not available, using mock store")
                self._initialize_mock()
                return
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=self.config.chroma_persist_directory
            )
            
            # Get or create collection
            try:
                self.chroma_collection = self.chroma_client.get_collection("alrouf_knowledge")
                logger.info("Connected to existing ChromaDB collection")
            except:
                self.chroma_collection = self.chroma_client.create_collection(
                    name="alrouf_knowledge",
                    metadata={"description": "Alrouf Lighting Technology Knowledge Base"}
                )
                logger.info("Created new ChromaDB collection")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            self._initialize_mock()
    
    def _initialize_mock(self):
        """Initialize mock vector store"""
        try:
            self.index = None
            self.metadata = []
            self.embeddings = []
            logger.info("Initialized mock vector store")
            
        except Exception as e:
            logger.error(f"Error initializing mock store: {e}")
    
    def store_embeddings(self, documents: List[Dict]) -> Dict:
        """
        Store embeddings in the vector database
        
        Args:
            documents: List of documents with embeddings
            
        Returns:
            Dictionary with storage results
        """
        try:
            logger.info(f"Storing {len(documents)} embeddings")
            
            if self.config.vector_db_type == "faiss":
                return self._store_in_faiss(documents)
            elif self.config.vector_db_type == "chroma":
                return self._store_in_chroma(documents)
            else:
                return self._store_in_mock(documents)
                
        except Exception as e:
            logger.error(f"Error storing embeddings: {e}")
            return {"status": "error", "message": str(e)}
    
    def _store_in_faiss(self, documents: List[Dict]) -> Dict:
        """Store embeddings in FAISS index"""
        try:
            if not self.index:
                logger.error("FAISS index not initialized")
                return {"status": "error", "message": "FAISS index not initialized"}
            
            # Extract embeddings and metadata
            embeddings = []
            for doc in documents:
                if "embedding" in doc:
                    embeddings.append(doc["embedding"])
                    self.metadata.append(doc["metadata"])
            
            if not embeddings:
                return {"status": "error", "message": "No embeddings found"}
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings, dtype=np.float32)
            
            # Add to index
            self.index.add(embeddings_array)
            
            # Save index and metadata
            self._save_faiss_index()
            self._save_metadata()
            
            logger.info(f"Stored {len(embeddings)} embeddings in FAISS")
            
            return {
                "status": "success",
                "stored_count": len(embeddings),
                "total_vectors": self.index.ntotal
            }
            
        except Exception as e:
            logger.error(f"Error storing in FAISS: {e}")
            return {"status": "error", "message": str(e)}
    
    def _store_in_chroma(self, documents: List[Dict]) -> Dict:
        """Store embeddings in ChromaDB"""
        try:
            if not self.chroma_collection:
                logger.error("ChromaDB collection not initialized")
                return {"status": "error", "message": "ChromaDB collection not initialized"}
            
            # Prepare data for ChromaDB
            ids = []
            embeddings = []
            metadatas = []
            documents_text = []
            
            for i, doc in enumerate(documents):
                if "embedding" in doc:
                    ids.append(f"doc_{i}")
                    embeddings.append(doc["embedding"])
                    metadatas.append(doc["metadata"])
                    documents_text.append(doc["content"])
            
            if not embeddings:
                return {"status": "error", "message": "No embeddings found"}
            
            # Add to collection
            self.chroma_collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents_text
            )
            
            logger.info(f"Stored {len(embeddings)} embeddings in ChromaDB")
            
            return {
                "status": "success",
                "stored_count": len(embeddings)
            }
            
        except Exception as e:
            logger.error(f"Error storing in ChromaDB: {e}")
            return {"status": "error", "message": str(e)}
    
    def _store_in_mock(self, documents: List[Dict]) -> Dict:
        """Store embeddings in mock store"""
        try:
            stored_count = 0
            
            for doc in documents:
                if "embedding" in doc:
                    self.embeddings.append(doc["embedding"])
                    self.metadata.append(doc["metadata"])
                    stored_count += 1
            
            logger.info(f"Stored {stored_count} embeddings in mock store")
            
            return {
                "status": "success",
                "stored_count": stored_count
            }
            
        except Exception as e:
            logger.error(f"Error storing in mock store: {e}")
            return {"status": "error", "message": str(e)}
    
    def search(self, query_embedding: List[float], max_results: int = 5) -> List[Dict]:
        """
        Search for similar embeddings
        
        Args:
            query_embedding: Query embedding vector
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with metadata
        """
        try:
            if self.config.vector_db_type == "faiss":
                return self._search_faiss(query_embedding, max_results)
            elif self.config.vector_db_type == "chroma":
                return self._search_chroma(query_embedding, max_results)
            else:
                return self._search_mock(query_embedding, max_results)
                
        except Exception as e:
            logger.error(f"Error searching embeddings: {e}")
            return []
    
    def _search_faiss(self, query_embedding: List[float], max_results: int) -> List[Dict]:
        """Search using FAISS index"""
        try:
            if not self.index or self.index.ntotal == 0:
                return []
            
            # Convert query to numpy array
            query_array = np.array([query_embedding], dtype=np.float32)
            
            # Search
            scores, indices = self.index.search(query_array, max_results)
            
            # Format results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.metadata):
                    result = {
                        "metadata": self.metadata[idx],
                        "score": float(score),
                        "index": int(idx)
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching FAISS: {e}")
            return []
    
    def _search_chroma(self, query_embedding: List[float], max_results: int) -> List[Dict]:
        """Search using ChromaDB"""
        try:
            if not self.chroma_collection:
                return []
            
            # Search
            results = self.chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results
            )
            
            # Format results
            formatted_results = []
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    result = {
                        "metadata": results["metadatas"][0][i],
                        "score": float(results["distances"][0][i]),
                        "content": results["documents"][0][i]
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []
    
    def _search_mock(self, query_embedding: List[float], max_results: int) -> List[Dict]:
        """Search using mock store"""
        try:
            if not self.embeddings:
                return []
            
            # Calculate similarities
            similarities = []
            for i, embedding in enumerate(self.embeddings):
                similarity = self._calculate_cosine_similarity(query_embedding, embedding)
                similarities.append((similarity, i))
            
            # Sort by similarity
            similarities.sort(reverse=True)
            
            # Return top results
            results = []
            for similarity, idx in similarities[:max_results]:
                if similarity >= self.config.similarity_threshold:
                    result = {
                        "metadata": self.metadata[idx],
                        "score": similarity,
                        "index": idx
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching mock store: {e}")
            return []
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            if not np:
                # Simple cosine similarity without numpy
                dot_product = sum(a * b for a, b in zip(vec1, vec2))
                norm1 = sum(a * a for a in vec1) ** 0.5
                norm2 = sum(b * b for b in vec2) ** 0.5
            
                if norm1 == 0 or norm2 == 0:
                    return 0.0
                
                return dot_product / (norm1 * norm2)
            
            # Using numpy for better performance
            vec1_array = np.array(vec1)
            vec2_array = np.array(vec2)
            
            dot_product = np.dot(vec1_array, vec2_array)
            norm1 = np.linalg.norm(vec1_array)
            norm2 = np.linalg.norm(vec2_array)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return float(dot_product / (norm1 * norm2))
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def _save_faiss_index(self):
        """Save FAISS index to disk"""
        try:
            if self.index:
                index_path = Path(self.config.faiss_index_path)
                index_path.parent.mkdir(parents=True, exist_ok=True)
                faiss.write_index(self.index, str(index_path))
                logger.info(f"Saved FAISS index to {index_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {e}")
    
    def _save_metadata(self):
        """Save metadata to disk"""
        try:
            metadata_path = Path(self.config.faiss_index_path).with_suffix('.metadata')
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            logger.info(f"Saved metadata to {metadata_path}")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
    
    def _load_metadata(self):
        """Load metadata from disk"""
        try:
            metadata_path = Path(self.config.faiss_index_path).with_suffix('.metadata')
            if metadata_path.exists():
                with open(metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
                logger.info(f"Loaded metadata from {metadata_path}")
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
    
    def get_document_count(self) -> int:
        """Get total number of documents"""
        try:
            if self.config.vector_db_type == "faiss" and self.index:
                return self.index.ntotal
            elif self.config.vector_db_type == "chroma" and self.chroma_collection:
                return self.chroma_collection.count()
            else:
                return len(self.metadata)
        except Exception:
            return 0
    
    def get_embedding_count(self) -> int:
        """Get total number of embeddings"""
        return self.get_document_count()
    
    def get_index_size(self) -> str:
        """Get index size in MB"""
        try:
            if self.config.vector_db_type == "faiss":
                index_path = Path(self.config.faiss_index_path)
                if index_path.exists():
                    size_bytes = index_path.stat().st_size
                    return f"{size_bytes / (1024 * 1024):.2f} MB"
            return "Unknown"
        except Exception:
            return "Unknown"
    
    def get_last_update_time(self) -> str:
        """Get last update time"""
        try:
            if self.config.vector_db_type == "faiss":
                index_path = Path(self.config.faiss_index_path)
                if index_path.exists():
                    timestamp = index_path.stat().st_mtime
                    return datetime.fromtimestamp(timestamp).isoformat()
            return "Unknown"
        except Exception:
            return "Unknown"
