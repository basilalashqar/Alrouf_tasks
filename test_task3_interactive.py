#!/usr/bin/env python3
"""
Interactive test script for Task 3 - RAG Knowledge Base
"""

import requests

question = input("Whats your question?")
language = input("Preferred Language (ar/en):")

# RAG query
rag_query = {
    "question": question,
    "language": language
}

response = requests.post("http://localhost:8000/rag/query", json=rag_query)
result = response.json()

print(f"Answer: {result['answer']}")
print(f"Confidence: {result['confidence']}%")
print(f"Sources: {result['sources']}")
