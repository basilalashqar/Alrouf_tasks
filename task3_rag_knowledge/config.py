"""
Configuration for RAG Knowledge Base
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration class for RAG Knowledge Base"""
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # Vector Database Configuration
    faiss_index_path: str = os.getenv("FAISS_INDEX_PATH", "./data/faiss_index")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "faiss")  # faiss, chroma, pgvector
    
    # Document Processing
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    max_document_size: int = int(os.getenv("MAX_DOCUMENT_SIZE", "10000000"))  # 10MB
    
    # Query Configuration
    max_results: int = int(os.getenv("MAX_RESULTS", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    
    # Language Support
    supported_languages: list = None
    default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["en", "ar"]
    
    # Mock Services
    use_mock_services: bool = os.getenv("USE_MOCK_SERVICES", "True").lower() == "true"
    mock_openai: bool = os.getenv("MOCK_OPENAI", "True").lower() == "true"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/rag_knowledge.log")
    
    # Performance
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))
    max_concurrent_requests: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.use_mock_services and not self.mock_openai:
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when not using mock services")
        
        # Validate chunk settings
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be positive")
        if self.chunk_overlap < 0:
            raise ValueError("CHUNK_OVERLAP must be non-negative")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be less than CHUNK_SIZE")
        
        # Validate vector database type
        if self.vector_db_type not in ["faiss", "chroma", "pgvector"]:
            raise ValueError("VECTOR_DB_TYPE must be one of: faiss, chroma, pgvector")
