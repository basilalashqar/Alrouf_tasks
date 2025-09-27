# Alrouf Lighting Technology - AI Automation Solutions

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start

**3 AI Solutions for Alrouf Lighting Technology:**
- **Task 1**: Zapier RFQ Automation (No-code)
- **Task 2**: Python Quotation Service + React Webapp
- **Task 3**: RAG Knowledge Base + React Webapp

**Both Python and Webapp work together!**

## 🎯 Task 1: RFQ Automation (No-Code)

**Zapier workflow** for email → CRM automation.

### Setup
1. Import `task1_rfq_automation/zapier_workflow/workflow_blueprint.json` into Zapier
2. Connect services: Gmail, OpenAI, Google Sheets, Salesforce, Google Drive, Slack
3. Test with sample email

### Test
```bash
python task1_rfq_automation/test_workflow.py
```

## 🎯 Task 2: Quotation Service

**FastAPI microservice** + **React webapp** for quotation generation.

### Python Usage
```bash
# Start API server
python simple_api_server.py

# Test with Python
python python_client_examples.py
```

### Webapp Usage
```bash
# Start API server (Terminal 1)
python simple_api_server.py

# Start webapp (Terminal 2)
cd webapp && npm start

# Access: http://localhost:3000/quotation
```

### API Example
```python
import requests

data = {
    "client": {"name": "Test", "contact": "test@test.com", "lang": "en"},
    "currency": "SAR",
    "items": [{"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240, "margin_pct": 22}]
}

response = requests.post("http://localhost:8000/quote", json=data)
print(response.json())
```

## 🎯 Task 3: RAG Knowledge Base

**AI Q&A system** with document processing and multi-language support.

### Python Usage
```bash
# Start API server
python simple_api_server.py

# Test queries
python -c "
import requests
response = requests.post('http://localhost:8000/rag/query', 
    json={'query': 'What products do you offer?', 'language': 'en'})
print(response.json())
"
```

### Webapp Usage
```bash
# Start API server (Terminal 1)
python simple_api_server.py

# Start webapp (Terminal 2)
cd webapp && npm start

# Access: http://localhost:3000/rag
```

### Arabic Support
```python
# Arabic queries work perfectly
response = requests.post('http://localhost:8000/rag/query', 
    json={'query': 'ما هي منتجاتكم؟', 'language': 'ar'})
print(response.json())
```

## 🧪 Testing

### Quick Test Everything
```bash
# Test all tasks
python test_all_tasks.py

# Test Python APIs
python python_client_examples.py

# Test webapp
# 1. python simple_api_server.py
# 2. cd webapp && npm start
# 3. Go to http://localhost:3000
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🛠️ Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/basilalashqar/Alrouf_tasks.git
cd Alrouf_tasks

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup webapp
cd webapp
npm install
```

### Environment Variables
```bash
cp env.example .env
# Edit .env with your API keys (optional for testing)
```

## 📊 Features

| Task | Python API | React Webapp | Arabic Support |
|------|------------|--------------|----------------|
| **Task 1** | N/A (Zapier) | N/A | ✅ |
| **Task 2** | ✅ | ✅ | ✅ |
| **Task 3** | ✅ | ✅ | ✅ |

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **API not responding** | `python simple_api_server.py` |
| **Webapp connection error** | Check API server is running |
| **Port conflicts** | `lsof -ti:8000 \| xargs kill -9` |
| **React won't start** | `npm cache clean --force && npm install` |

## 📚 Documentation

- [Task 1 Details](docs/task1_rfq_automation.md)
- [Task 2 Details](docs/task2_quotation_service.md)
- [Task 3 Details](docs/task3_rag_knowledge.md)
- [Project Summary](PROJECT_SUMMARY.md)

## 🚀 Deployment

### Production Setup
1. **Task 1**: Configure production Zapier account
2. **Task 2**: Deploy FastAPI with Docker
3. **Task 3**: Deploy RAG system with vector database

### Docker
```bash
# Task 2
docker build -t alrouf-quotation task2_quotation_service/
docker run -p 8000:8000 alrouf-quotation

# Task 3
docker build -t alrouf-rag task3_rag_knowledge/
docker run -p 8080:8080 alrouf-rag
```

## 📞 Support

- **Email**: basil@alrouf.com
- **GitHub Issues**: [Create an issue](https://github.com/basilalashqar/Alrouf_tasks/issues)
- **Repository**: https://github.com/basilalashqar/Alrouf_tasks

---

**Built with ❤️ for Alrouf Lighting Technology**