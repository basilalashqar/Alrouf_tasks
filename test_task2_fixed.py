#!/usr/bin/env python3
"""
Fixed test script for Task 2 - Quotation Service
"""

import requests
import json
import os
from datetime import datetime

def test_quotation_service():
    """Test the quotation service API"""
    
    print("🧪 Testing Task 2: Quotation Service")
    print("=" * 50)
    
    # Test quotation generation
    quotation_data = {
        "client": {
            "name": "Gulf Engineering",
            "contact": "omar@client.com",
            "lang": "en"
        },
        "currency": "SAR",
        "items": [
            {
                "sku": "ALR-SL-90W",
                "qty": 120,
                "unit_cost": 240.0,
                "margin_pct": 22
            },
            {
                "sku": "ALR-OBL-12V",
                "qty": 40,
                "unit_cost": 95.5,
                "margin_pct": 18
            }
        ],
        "delivery_terms": "DAP Dammam, 4 weeks",
        "notes": "Client requested Tarsheed compliance"
    }
    
    try:
        print("📤 Sending quotation request...")
        response = requests.post("http://localhost:8000/quote", json=quotation_data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Quotation generated successfully!")
            print(f"📋 Quotation ID: {result['quotation_id']}")
            print(f"👤 Client: {result['client']['name']}")
            print(f"💰 Subtotal: {result['subtotal']} SAR")
            print(f"📊 Tax Amount: {result['tax_amount']} SAR")
            print(f"💵 Total: {result['total']} SAR")
            print(f"📧 Email Draft Length: {len(result['email_draft'])} characters")
            
            # Show item details
            print("\n📦 Item Details:")
            for item in result['items']:
                print(f"  - {item['sku']}: {item['qty']} pcs × {item['unit_price']} = {item['line_total']} SAR")
            
            print("\n📧 Email Draft Preview:")
            print("-" * 40)
            print(result['email_draft'][:200] + "..." if len(result['email_draft']) > 200 else result['email_draft'])
            print("-" * 40)
            
            # Generate email report
            generate_email_report(result)
            
            return True
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server")
        print("Make sure the API server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    
    print("\n🔍 Testing Health Check...")
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

def generate_email_report(result):
    """Generate a detailed email report"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"email_report_{timestamp}.txt"
    
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ALROUF LIGHTING TECHNOLOGY - EMAIL DRAFT REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Quotation ID: {result['quotation_id']}\n")
            f.write(f"Client: {result['client']['name']} ({result['client']['contact']})\n")
            f.write(f"Language: {result['client']['lang'].upper()}\n")
            f.write(f"Total Amount: {result['total']} SAR\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("EMAIL DRAFT:\n")
            f.write("-" * 40 + "\n")
            f.write(result['email_draft'])
            f.write("\n" + "-" * 40 + "\n\n")
            
            f.write("QUOTATION DETAILS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Subtotal: {result['subtotal']} SAR\n")
            f.write(f"Tax Amount: {result['tax_amount']} SAR\n")
            f.write(f"Total: {result['total']} SAR\n\n")
            
            f.write("ITEMS:\n")
            for item in result['items']:
                f.write(f"- {item['sku']}: {item['qty']} pcs × {item['unit_price']} = {item['line_total']} SAR\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"📄 Email report saved: {report_filename}")
        print(f"📊 Report size: {os.path.getsize(report_filename)} bytes")
        
    except Exception as e:
        print(f"❌ Error generating email report: {e}")

if __name__ == "__main__":
    print("🚀 Alrouf Lighting Technology - Task 2 Testing")
    print("=" * 60)
    
    # Test health check first
    health_ok = test_health_check()
    
    if health_ok:
        # Test quotation service
        quotation_ok = test_quotation_service()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS:")
        print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"Quotation Service: {'✅ PASS' if quotation_ok else '❌ FAIL'}")
        
        if health_ok and quotation_ok:
            print("\n🎉 All tests passed! Task 2 is working correctly.")
        else:
            print("\n⚠️  Some tests failed. Check the errors above.")
    else:
        print("\n❌ Cannot test quotation service - API server is not running")
        print("Start the API server with: python3 simple_api_server.py")
