#!/usr/bin/env python3
"""
Task 3: RAG Knowledge Base
Retrieval-Augmented Generation system with AR/EN support
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# Import our modules
from document_processor import DocumentProcessor
from embedding_service import EmbeddingService
from vector_store import VectorStore
from query_engine import QueryEngine
from config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/rag_knowledge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RAGKnowledgeBase:
    """Main RAG Knowledge Base system"""
    
    def __init__(self):
        self.config = Config()
        self.document_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.query_engine = QueryEngine()
        
        # Initialize components
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the RAG system"""
        try:
            # Create necessary directories
            Path("data").mkdir(exist_ok=True)
            Path("logs").mkdir(exist_ok=True)
            Path("documents").mkdir(exist_ok=True)
            
            # Initialize vector store (method doesn't exist in mock mode)
            # self.vector_store.initialize()
            
            logger.info("RAG Knowledge Base initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
            raise
    
    def ingest_documents(self, documents_dir: str = "documents") -> Dict:
        """
        Ingest documents into the knowledge base
        
        Args:
            documents_dir: Directory containing documents to ingest
            
        Returns:
            Dictionary with ingestion results
        """
        try:
            logger.info(f"Ingesting documents from {documents_dir}")
            
            # Process documents
            documents = self.document_processor.process_directory(documents_dir)
            logger.info(f"Processed {len(documents)} documents")
            
            # Generate embeddings
            embeddings = self.embedding_service.generate_embeddings(documents)
            logger.info(f"Generated {len(embeddings)} embeddings")
            
            # Store in vector database
            store_result = self.vector_store.store_embeddings(embeddings, documents)
            logger.info(f"Stored embeddings in vector database")
            
            # Save metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "documents_processed": len(documents),
                "embeddings_generated": len(embeddings),
                "documents": [doc["metadata"] for doc in documents]
            }
            
            with open("logs/ingestion_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.info("Document ingestion completed successfully")
            
            return {
                "status": "success",
                "documents_processed": len(documents),
                "embeddings_generated": len(embeddings),
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            return {"status": "error", "message": str(e)}
    
    def query(self, question: str, language: str = "en", max_results: int = 5) -> Dict:
        """
        Query the knowledge base
        
        Args:
            question: Question to ask
            language: Language preference (en/ar)
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            logger.info(f"Processing query: {question} (language: {language})")
            
            # Generate query embedding
            query_embedding = self.embedding_service.generate_query_embedding(question)
            
            # Search vector database
            search_results = self.vector_store.search(query_embedding, max_results)
            
            # Generate answer using retrieved context
            answer = self.query_engine.generate_answer(
                question, 
                search_results, 
                language
            )
            
            # Format response
            response = {
                "question": question,
                "answer": answer["answer"],
                "sources": answer["sources"],
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "confidence": answer.get("confidence", 0.0)
            }
            
            logger.info(f"Query processed successfully: {len(answer['sources'])} sources")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "question": question,
                "answer": "Sorry, I encountered an error processing your question.",
                "sources": [],
                "language": language,
                "error": str(e)
            }
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        try:
            stats = {
                "total_documents": self.vector_store.get_document_count(),
                "total_embeddings": self.vector_store.get_embedding_count(),
                "index_size": self.vector_store.get_index_size(),
                "last_updated": self.vector_store.get_last_update_time(),
                "system_status": "healthy"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {"system_status": "error", "message": str(e)}
    
    def run_cli_interface(self):
        """Run CLI interface for Q&A"""
        print("🤖 Alrouf Lighting Technology - RAG Knowledge Base")
        print("=" * 60)
        print("Ask questions about our products and services!")
        print("Type 'quit' to exit, 'stats' for system statistics")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                question = input("\n💬 Your question: ").strip()
                
                if question.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                
                if question.lower() == 'stats':
                    stats = self.get_system_stats()
                    print(f"\n📊 System Statistics:")
                    print(f"   Documents: {stats.get('total_documents', 0)}")
                    print(f"   Embeddings: {stats.get('total_embeddings', 0)}")
                    print(f"   Status: {stats.get('system_status', 'unknown')}")
                    continue
                
                if not question:
                    continue
                
                # Detect language
                language = "ar" if any(char in question for char in "أبتثجحخدذرزسشصضطظعغفقكلمنهوي") else "en"
                
                # Process query
                print(f"\n🔍 Processing query in {language.upper()}...")
                result = self.query(question, language)
                
                # Display results
                print(f"\n📝 Answer:")
                print(f"   {result['answer']}")
                
                if result.get('sources'):
                    print(f"\n📚 Sources ({len(result['sources'])}):")
                    for i, source in enumerate(result['sources'], 1):
                        print(f"   {i}. {source.get('title', 'Unknown')} (Score: {source.get('score', 0):.3f})")
                
                if result.get('confidence'):
                    print(f"\n🎯 Confidence: {result['confidence']:.2f}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main entry point"""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Initialize RAG system
    rag = RAGKnowledgeBase()
    
    # Check if documents exist
    documents_dir = Path("documents")
    if not documents_dir.exists() or not any(documents_dir.iterdir()):
        print("📁 No documents found in 'documents' directory.")
        print("Please add some documents first, then run the ingestion process.")
        return
    
    # Ingest documents if not already done
    print("📚 Ingesting documents...")
    ingestion_result = rag.ingest_documents()
    
    if ingestion_result["status"] == "success":
        print(f"✅ Successfully ingested {ingestion_result['documents_processed']} documents")
    else:
        print(f"❌ Error ingesting documents: {ingestion_result.get('message', 'Unknown error')}")
        return
    
    # Run CLI interface
    rag.run_cli_interface()

if __name__ == "__main__":
    main()
