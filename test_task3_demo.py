#!/usr/bin/env python3
"""
Demo test script for Task 3 - RAG Knowledge Base
"""

import requests

# Demo queries
queries = [
    {"question": "What products do you offer?", "language": "en"},
    {"question": "ما هي المنتجات التي تقدمونها؟", "language": "ar"},
    {"question": "What is the warranty policy?", "language": "en"},
    {"question": "ما هي سياسة الضمان؟", "language": "ar"}
]

for query in queries:
    print(f"\nQuestion: {query['question']}")
    print(f"Language: {query['language']}")
    
    response = requests.post("http://localhost:8000/rag/query", json=query)
    result = response.json()
    
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Sources: {result['sources']}")
    print("-" * 50)
