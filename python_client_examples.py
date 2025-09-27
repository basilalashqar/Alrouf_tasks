#!/usr/bin/env python3
"""
Python Client Examples for Alrouf AI Services
Demonstrates how to use the Python API directly
"""

import requests
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"

def generate_quotation_python(client_name, contact, language="en", currency="SAR", items=None):
    """
    Generate quotation using Python API call
    
    Args:
        client_name (str): Client name
        contact (str): Client contact email
        language (str): Language preference (en/ar)
        currency (str): Currency code
        items (list): List of items with sku, qty, unit_cost, margin_pct
    
    Returns:
        dict: Quotation response
    """
    if items is None:
        items = [
            {"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
            {"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
        ]
    
    quotation_data = {
        "client": {
            "name": client_name,
            "contact": contact,
            "lang": language
        },
        "currency": currency,
        "items": items,
        "delivery_terms": "DAP Dammam, 4 weeks",
        "notes": "Generated via Python API"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/quote", json=quotation_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating quotation: {e}")
        return None

def query_rag_python(question, language="en"):
    """
    Query RAG knowledge base using Python API call
    
    Args:
        question (str): Question to ask
        language (str): Language preference (en/ar)
    
    Returns:
        dict: RAG response
    """
    rag_data = {
        "query": question,
        "language": language
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/rag/query", json=rag_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying RAG: {e}")
        return None

def check_api_health():
    """Check if API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function demonstrating Python API usage"""
    print("🐍 Alrouf AI - Python Client Examples")
    print("=" * 50)
    
    # Check API health
    if not check_api_health():
        print("❌ API server is not running!")
        print("   Please start the API server first:")
        print("   python simple_api_server.py")
        return
    
    print("✅ API server is running!")
    print()
    
    # Example 1: Generate Quotation
    print("📊 Example 1: Generate Quotation")
    print("-" * 40)
    
    quotation = generate_quotation_python(
        client_name="Gulf Engineering",
        contact="omar@gulfeng.com",
        language="en",
        currency="SAR"
    )
    
    if quotation:
        print(f"✅ Quotation Generated: {quotation['quotation_id']}")
        print(f"   Total: {quotation['currency']} {quotation['total']}")
        print(f"   Client: {quotation['client']['name']}")
        print(f"   Email Draft: {len(quotation['email_draft'])} characters")
    else:
        print("❌ Failed to generate quotation")
    
    print()
    
    # Example 2: RAG Query
    print("🧠 Example 2: RAG Knowledge Base Query")
    print("-" * 40)
    
    rag_response = query_rag_python(
        question="What products do you offer?",
        language="en"
    )
    
    if rag_response:
        print(f"✅ RAG Query Successful:")
        print(f"   Answer: {rag_response['answer'][:100]}...")
        print(f"   Confidence: {rag_response['confidence']}%")
        print(f"   Sources: {len(rag_response['sources'])} found")
    else:
        print("❌ Failed to query RAG")
    
    print()
    
    # Example 3: Arabic Query
    print("🌍 Example 3: Arabic RAG Query")
    print("-" * 40)
    
    arabic_response = query_rag_python(
        question="ما هي منتجاتكم؟",
        language="ar"
    )
    
    if arabic_response:
        print(f"✅ Arabic Query Successful:")
        print(f"   Answer: {arabic_response['answer'][:100]}...")
        print(f"   Confidence: {arabic_response['confidence']}%")
    else:
        print("❌ Failed to query Arabic RAG")
    
    print()
    print("🎯 Python API Usage Complete!")
    print("   You can use these functions in your own scripts")
    print("   Or use the React webapp at: http://localhost:3000")

if __name__ == "__main__":
    main()
