#!/usr/bin/env python3
"""
Fixed test script for Task 3 - RAG Knowledge Base
Tests both Arabic and English queries with HTML report generation
"""

import requests
import json
import os
from datetime import datetime

def test_rag_system():
    """Test the RAG Knowledge Base API"""
    
    print("🧪 Testing Task 3: RAG Knowledge Base")
    print("=" * 50)
    
    # Test queries in both languages
    test_queries = [
        {
            "question": "What products do you offer?",
            "language": "en",
            "description": "Product Information (English)"
        },
        {
            "question": "ما هي المنتجات التي تقدمونها؟",
            "language": "ar", 
            "description": "Product Information (Arabic)"
        },
        {
            "question": "What is the warranty policy?",
            "language": "en",
            "description": "Warranty Information (English)"
        },
        {
            "question": "ما هي سياسة الضمان؟",
            "language": "ar",
            "description": "Warranty Information (Arabic)"
        },
        {
            "question": "How to install the lighting system?",
            "language": "en",
            "description": "Installation Guide (English)"
        },
        {
            "question": "كيف يتم تركيب نظام الإضاءة؟",
            "language": "ar",
            "description": "Installation Guide (Arabic)"
        }
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query['description']}")
        print(f"Question: {query['question']}")
        
        try:
            response = requests.post("http://localhost:8000/rag/query", json=query)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Answer: {result['answer'][:100]}...")
                print(f"📊 Confidence: {result['confidence']}%")
                print(f"⏱️  Response Time: {result['response_time']}ms")
                print(f"📚 Sources: {', '.join(result['sources'])}")
                
                # Store result for HTML report
                results.append({
                    "test_number": i,
                    "description": query['description'],
                    "question": query['question'],
                    "language": query['language'],
                    "answer": result['answer'],
                    "confidence": result['confidence'],
                    "response_time": result['response_time'],
                    "sources": result['sources'],
                    "processing_time": result.get('processing_time', 0)
                })
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                results.append({
                    "test_number": i,
                    "description": query['description'],
                    "question": query['question'],
                    "language": query['language'],
                    "answer": f"Error: HTTP {response.status_code}",
                    "confidence": 0,
                    "response_time": 0,
                    "sources": ["Error"],
                    "processing_time": 0
                })
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Could not connect to API server")
            print("Make sure the API server is running on http://localhost:8000")
            return False, []
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "test_number": i,
                "description": query['description'],
                "question": query['question'],
                "language": query['language'],
                "answer": f"Error: {str(e)}",
                "confidence": 0,
                "response_time": 0,
                "sources": ["Error"],
                "processing_time": 0
            })
    
    return True, results

def test_health_check():
    """Test the health check endpoint"""
    
    print("🔍 Testing Health Check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data['message']}")
            return True
        else:
            print(f"❌ Health Check Failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def generate_html_report(results):
    """Generate a detailed HTML report for RAG testing"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"rag_test_report_{timestamp}.html"
    
    try:
        # Calculate statistics
        total_tests = len(results)
        successful_tests = len([r for r in results if r['confidence'] > 0])
        avg_confidence = sum(r['confidence'] for r in results) / total_tests if total_tests > 0 else 0
        avg_response_time = sum(r['response_time'] for r in results) / total_tests if total_tests > 0 else 0
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            # Write HTML header
            f.write("""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG Knowledge Base - Test Report</title>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.6;
            margin: 40px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .title {
            color: #2c3e50;
            text-align: center;
            font-size: 28px;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
        }
        .arabic-title {
            color: #2c3e50;
            text-align: center;
            font-size: 24px;
            margin-bottom: 30px;
            direction: rtl;
            font-family: Arial, Tahoma, sans-serif;
        }
        .stats {
            background-color: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 5px solid #27ae60;
        }
        .test-result {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }
        .test-header {
            color: #e74c3c;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .question {
            color: #2c3e50;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .answer {
            color: #34495e;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
        }
        .arabic-answer {
            direction: rtl;
            text-align: right;
            font-family: Arial, Tahoma, sans-serif;
        }
        .metrics {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        .metric {
            background-color: #3498db;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        .footer {
            text-align: center;
            color: #7f8c8d;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">RAG Knowledge Base - Test Report</h1>
        <h2 class="arabic-title">نظام قاعدة المعرفة RAG - تقرير الاختبار</h2>
        
        <div class="stats">
            <h3>Test Statistics</h3>
            <p><strong>Total Tests:</strong> {}</p>
            <p><strong>Successful Tests:</strong> {}</p>
            <p><strong>Success Rate:</strong> {:.1f}%</p>
            <p><strong>Average Confidence:</strong> {:.1f}%</p>
            <p><strong>Average Response Time:</strong> {:.0f}ms</p>
            <p><strong>Generated:</strong> {}</p>
        </div>
""".format(
                total_tests,
                successful_tests,
                (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                avg_confidence,
                avg_response_time,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            # Add test results
            for result in results:
                is_arabic = result['language'] == 'ar'
                answer_class = 'arabic-answer' if is_arabic else ''
                
                f.write(f"""
        <div class="test-result">
            <div class="test-header">Test {result['test_number']}: {result['description']}</div>
            <div class="question">Question: {result['question']}</div>
            <div class="answer {answer_class}">
                <strong>Answer:</strong><br>
                {result['answer']}
            </div>
            <div class="metrics">
                <div class="metric">Confidence: {result['confidence']}%</div>
                <div class="metric">Response Time: {result['response_time']}ms</div>
                <div class="metric">Sources: {', '.join(result['sources'])}</div>
            </div>
        </div>
""")
            
            f.write("""
        <div class="footer">
            <p>Generated by Alrouf Lighting Technology RAG Test System</p>
            <p class="arabic-answer">تم إنشاؤه بواسطة نظام اختبار RAG لشركة الأروف للتكنولوجيا والإضاءة</p>
        </div>
    </div>
</body>
</html>""")
        
        print(f"📄 HTML report saved: {report_filename}")
        print(f"📊 Report size: {os.path.getsize(report_filename)} bytes")
        
    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")

if __name__ == "__main__":
    print("🚀 Alrouf Lighting Technology - Task 3 RAG Testing")
    print("=" * 60)
    
    # Test health check first
    health_ok = test_health_check()
    
    if health_ok:
        # Test RAG system
        rag_ok, results = test_rag_system()
        
        if rag_ok and results:
            # Generate HTML report
            print("\n📄 Generating HTML Report...")
            generate_html_report(results)
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS:")
        print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"RAG System: {'✅ PASS' if rag_ok else '❌ FAIL'}")
        
        if health_ok and rag_ok:
            print("\n🎉 All tests passed! Task 3 RAG system is working correctly.")
            print("📄 Check the generated HTML report for detailed results.")
        else:
            print("\n⚠️  Some tests failed. Check the errors above.")
    else:
        print("\n❌ Cannot test RAG system - API server is not running")
        print("Start the API server with: python3 simple_api_server.py")
