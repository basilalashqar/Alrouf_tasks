# Alrouf Lighting Technology - Task Solutions

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Complete automation suite for Alrouf Lighting Technology featuring:
- **Task 2**: Python Quotation Service + React Webapp
- **Task 3**: RAG Knowledge Base + React Webapp

## Quick Start

### 1. Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python3 simple_api_server.py
```

### 3. Test Services

**Task 2 - Quotation Service:**
```bash
python3 test_task2_simple.py
```

**Task 3 - RAG Knowledge Base:**
```bash
python3 test_task3_interactive.py
```

### 4. Start React Webapp
```bash
cd webapp
npm install
npm start
```

## Project Structure

```
├── task2_quotation_service/     # Quotation API service
├── task3_rag_knowledge/         # RAG knowledge base
├── webapp/                      # React web application
├── test_task2_simple.py         # Simple quotation test
├── test_task3_interactive.py    # Interactive RAG test
├── simple_api_server.py         # Mock API server
└── requirements.txt             # Python dependencies
```

## Features

### Task 2 - Quotation Service
- ✅ FastAPI microservice with automatic pricing calculations
- ✅ Professional email generation (English/Arabic)
- ✅ RESTful API with OpenAPI documentation
- ✅ React webapp interface

### Task 3 - RAG Knowledge Base
- ✅ Advanced RAG system with vector embeddings
- ✅ Perfect Arabic language support with RTL formatting
- ✅ Source citations and confidence scoring
- ✅ React webapp interface

## API Endpoints

- **Health Check**: `GET http://localhost:8000/health`
- **Quotation**: `POST http://localhost:8000/quote`
- **RAG Query**: `POST http://localhost:8000/rag/query`
- **API Docs**: `http://localhost:8000/docs`

## Testing

### Simple Tests
```bash
# Test quotation service
python3 test_task2_simple.py

# Test RAG system interactively
python3 test_task3_interactive.py
```

### Webapp Testing
1. Start API server: `python3 simple_api_server.py`
2. Start webapp: `cd webapp && npm start`
3. Open: `http://localhost:3000`

## Requirements

- Python 3.13+
- Node.js 18+
- FastAPI, Uvicorn, Requests
- React, Axios

## License

MIT License - see [LICENSE](LICENSE) file for details.

## GitHub Repository

https://github.com/basilalashqar/Alrouf_tasks