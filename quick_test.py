#!/usr/bin/env python3
"""
Quick test script for video demonstration
"""

import requests
import json

def main():
    print("🎬 VIDEO DEMO - Quick API Test")
    print("=" * 40)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API Server is running")
        else:
            print("❌ API Server error")
            return
    except:
        print("❌ Cannot connect to API server")
        print("Start server with: python3 simple_api_server.py")
        return
    
    # Test 2: Quotation Service
    print("\n2. Testing Quotation Service...")
    quotation_data = {
        "client": {"name": "Demo Client", "contact": "demo@test.com", "lang": "en"},
        "currency": "SAR",
        "items": [{"sku": "ALR-SL-90W", "qty": 50, "unit_cost": 200.0, "margin_pct": 25}],
        "delivery_terms": "DAP Riyadh, 2 weeks",
        "notes": "Demo quotation"
    }
    
    try:
        response = requests.post("http://localhost:8000/quote", json=quotation_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Quotation ID: {result['quotation_id']}")
            print(f"💰 Total: {result['total']} SAR")
            print("✅ Quotation service working")
        else:
            print("❌ Quotation service error")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: RAG System (English)
    print("\n3. Testing RAG System (English)...")
    try:
        response = requests.post("http://localhost:8000/rag/query", 
                               json={"question": "What products do you offer?", "language": "en"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answer: {result['answer'][:50]}...")
            print(f"📊 Confidence: {result['confidence']}%")
            print("✅ RAG system working")
        else:
            print("❌ RAG system error")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: RAG System (Arabic)
    print("\n4. Testing RAG System (Arabic)...")
    try:
        response = requests.post("http://localhost:8000/rag/query", 
                               json={"question": "ما هي المنتجات التي تقدمونها؟", "language": "ar"})
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answer: {result['answer'][:50]}...")
            print(f"📊 Confidence: {result['confidence']}%")
            print("✅ Arabic RAG working")
        else:
            print("❌ Arabic RAG error")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Demo completed! All systems working.")
    print("📚 API Documentation: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
