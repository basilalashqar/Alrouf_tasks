# Task 3: RAG Knowledge Base

## Overview
A Retrieval-Augmented Generation (RAG) system that provides intelligent Q&A capabilities over company documents with support for Arabic and English languages.

## Features

### Document Processing
- **Multi-format Support**: PDF, DOCX, TXT, CSV, JSON, Markdown
- **Intelligent Chunking**: Optimal text segmentation for embeddings
- **Language Detection**: Automatic Arabic/English detection
- **Metadata Extraction**: Rich document metadata

### Vector Database
- **FAISS Integration**: High-performance similarity search
- **ChromaDB Support**: Alternative vector database option
- **Embedding Storage**: Efficient vector storage and retrieval
- **Similarity Search**: Fast nearest neighbor search

### Query Processing
- **Natural Language Queries**: Human-like question processing
- **Context Retrieval**: Relevant document sections
- **Answer Generation**: OpenAI-powered response generation
- **Source Citation**: Transparent source attribution

### Multi-language Support
- **Arabic Support**: Full Arabic language processing
- **English Support**: Native English language support
- **Language Detection**: Automatic language identification
- **Bilingual Responses**: Mixed language query handling

## Architecture

```
Documents → Processing → Embeddings → Vector Store → Query → Answer
    ↓           ↓           ↓           ↓         ↓       ↓
  Chunking → Embedding → FAISS/Chroma → Search → Context → Response
```

## Document Ingestion

### Supported Formats
- **PDF**: Text extraction from PDF documents
- **DOCX**: Microsoft Word document processing
- **TXT**: Plain text files
- **CSV**: Comma-separated value files
- **JSON**: Structured data files
- **Markdown**: Markdown formatted documents

### Processing Pipeline
1. **Document Loading**: Read documents from directory
2. **Text Extraction**: Extract text content from various formats
3. **Chunking**: Split documents into optimal chunks
4. **Embedding Generation**: Create vector embeddings
5. **Vector Storage**: Store embeddings in vector database
6. **Indexing**: Build searchable index

### Chunking Strategy
- **Size-based**: Configurable chunk size (default: 1000 characters)
- **Overlap**: Chunk overlap for context preservation (default: 200 characters)
- **Sentence-aware**: Respects sentence boundaries
- **Language-aware**: Handles Arabic and English text properly

## Vector Database

### FAISS Integration
- **IndexFlatIP**: Inner product similarity for cosine similarity
- **Persistent Storage**: Index saved to disk for persistence
- **Batch Operations**: Efficient batch embedding storage
- **Metadata Storage**: Document metadata alongside vectors

### ChromaDB Alternative
- **Persistent Client**: Long-term storage capabilities
- **Collection Management**: Organized document collections
- **Metadata Support**: Rich metadata storage
- **Query Interface**: Advanced query capabilities

### Embedding Models
- **OpenAI Embeddings**: text-embedding-ada-002 model
- **Mock Embeddings**: Deterministic mock embeddings for testing
- **Batch Processing**: Efficient batch embedding generation
- **Similarity Calculation**: Cosine similarity computation

## Query Engine

### Query Processing
1. **Query Embedding**: Convert question to vector
2. **Vector Search**: Find similar document chunks
3. **Context Retrieval**: Gather relevant context
4. **Answer Generation**: Generate response using OpenAI
5. **Source Attribution**: Provide source citations

### Answer Generation
- **OpenAI Integration**: GPT-3.5-turbo for answer generation
- **Context-aware**: Uses retrieved document context
- **Language-specific**: Arabic and English responses
- **Template Fallback**: Template-based responses when OpenAI unavailable

### Source Citation
- **Document Attribution**: Links to source documents
- **Relevance Scoring**: Similarity scores for sources
- **Metadata Display**: File names, types, and timestamps
- **Confidence Metrics**: Answer confidence scoring

## Usage

### CLI Interface
```bash
# Run the RAG system
python task3_rag_knowledge/main.py

# Interactive Q&A session
🤖 Alrouf Lighting Technology - RAG Knowledge Base
============================================================
Ask questions about our products and services!
Type 'quit' to exit, 'stats' for system statistics
============================================================

💬 Your question: What products do you offer?

📝 Answer:
Based on the information available in our knowledge base, we offer:

1. Streetlight Poles (ALR-SL Series)
   - ALR-SL-60W: 60W LED streetlight pole
   - ALR-SL-90W: 90W LED streetlight pole
   - ALR-SL-120W: 120W LED streetlight pole

2. Outdoor Bollard Lights (ALR-OBL Series)
   - ALR-OBL-12V: 12V outdoor bollard light

3. Flood Lights (ALR-FL Series)
   - ALR-FL-50W: 50W flood light

📚 Sources (3):
   1. alrouf_products.txt (Score: 0.892)
   2. installation_guide.txt (Score: 0.756)
   3. warranty_terms.txt (Score: 0.634)

🎯 Confidence: 0.89
```

### Programmatic Usage
```python
from task3_rag_knowledge.main import RAGKnowledgeBase

# Initialize RAG system
rag = RAGKnowledgeBase()

# Ingest documents
result = rag.ingest_documents("documents/")

# Query the system
response = rag.query("What is the warranty period?", language="en")
print(response["answer"])
```

## Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002

# Vector Database
VECTOR_DB_TYPE=faiss  # faiss, chroma, pgvector
FAISS_INDEX_PATH=./data/faiss_index
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_DOCUMENT_SIZE=10000000

# Query Configuration
MAX_RESULTS=5
SIMILARITY_THRESHOLD=0.7
DEFAULT_LANGUAGE=en

# Mock Services
USE_MOCK_SERVICES=True
MOCK_OPENAI=True
```

## Sample Documents

### Product Catalog
Comprehensive product information including:
- Product specifications
- Technical details
- Application guidelines
- Pricing information

### Installation Guide
Detailed installation procedures:
- Safety requirements
- Site preparation
- Foundation specifications
- Electrical connections
- Commissioning procedures

### Warranty Terms
Complete warranty information:
- Coverage details
- Claims process
- Documentation requirements
- Service procedures

## Performance

### Optimization Features
- **Batch Processing**: Efficient batch operations
- **Caching**: Response caching for repeated queries
- **Index Optimization**: Optimized vector search
- **Memory Management**: Efficient memory usage

### Performance Metrics
- **Query Latency**: Average response time
- **Index Size**: Vector database size
- **Memory Usage**: System memory consumption
- **Throughput**: Queries per second

## Testing

### Test Coverage
- **Document Processing**: All supported formats
- **Embedding Generation**: Vector creation and storage
- **Query Processing**: Question answering
- **Error Handling**: Failure scenarios

### Mock Services
- **Mock OpenAI**: Template-based responses
- **Mock Embeddings**: Deterministic mock vectors
- **Mock Vector Store**: In-memory vector storage
- **Mock Documents**: Sample document processing

## Monitoring

### System Statistics
```python
# Get system stats
stats = rag.get_system_stats()
print(f"Documents: {stats['total_documents']}")
print(f"Embeddings: {stats['total_embeddings']}")
print(f"Index Size: {stats['index_size']}")
print(f"Status: {stats['system_status']}")
```

### Logging
- **Processing Logs**: Document ingestion tracking
- **Query Logs**: Question processing history
- **Error Logs**: Detailed error information
- **Performance Logs**: Timing and metrics

## Security

### Data Protection
- **Local Processing**: All processing done locally
- **Secure Storage**: Encrypted vector storage
- **Access Control**: File system permissions
- **Audit Logging**: Complete operation tracking

### Privacy
- **No External Storage**: All data stays local
- **Secure Embeddings**: No sensitive data in vectors
- **Access Logs**: Query and access tracking
- **Data Retention**: Configurable data retention

## Maintenance

### Regular Tasks
- **Index Updates**: Regular index rebuilding
- **Document Sync**: Keep documents current
- **Performance Monitoring**: Regular performance checks
- **Log Analysis**: Daily log review

### Troubleshooting
- **Common Issues**: Documented solutions
- **Debug Procedures**: Step-by-step debugging
- **Recovery Procedures**: System recovery guides
- **Support Contacts**: Technical support information

## Future Enhancements

### Planned Features
- **Web Interface**: Browser-based Q&A interface
- **API Endpoints**: RESTful API for integration
- **Advanced Search**: Semantic search capabilities
- **Multi-modal**: Image and document processing

### Scalability
- **Distributed Processing**: Multi-node processing
- **Cloud Integration**: Cloud-based vector storage
- **Real-time Updates**: Live document updates
- **Advanced Analytics**: Usage analytics and insights
