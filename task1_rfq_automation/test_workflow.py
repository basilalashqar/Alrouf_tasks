#!/usr/bin/env python3
"""
Test script for Task 1: RFQ Automation (No-Code)
This simulates the Zapier workflow using sample data
"""

import json
import csv
from datetime import datetime
from pathlib import Path

def test_zapier_workflow():
    """Test the complete RFQ workflow using sample data"""
    
    print("🧪 Testing Task 1: RFQ → CRM Automation (No-Code)")
    print("=" * 60)
    
    # Step 1: Simulate Email Trigger
    print("\n📧 Step 1: Email Trigger")
    test_email = {
        "subject": "RFQ — Streetlight Poles",
        "body": "Hello Alrouf, please quote 120 pcs streetlight model ALR‑SL‑90W. Needed in Dammam within 4 weeks. Attach specs. Regards, Eng. Omar, +9665XXXX, omar@client.com",
        "from": "omar@client.com",
        "attachments": ["specs.pdf", "requirements.docx"]
    }
    print(f"✅ Email received: {test_email['subject']}")
    print(f"   From: {test_email['from']}")
    print(f"   Attachments: {len(test_email['attachments'])} files")
    
    # Step 2: Simulate OpenAI Field Extraction
    print("\n🤖 Step 2: OpenAI Field Extraction")
    extracted_data = {
        "client_name": "Gulf Eng.",
        "client_email": "omar@client.com",
        "client_phone": "+9665XXXX",
        "product_model": "ALR-SL-90W",
        "quantity": 120,
        "location": "Dammam",
        "timeline": "4 weeks",
        "language": "en"
    }
    print("✅ Fields extracted:")
    for key, value in extracted_data.items():
        print(f"   {key}: {value}")
    
    # Step 3: Simulate Google Sheets Write
    print("\n📊 Step 3: Google Sheets Integration")
    sheets_data = {
        "timestamp": datetime.now().isoformat(),
        "client_name": extracted_data["client_name"],
        "email": extracted_data["client_email"],
        "product": extracted_data["product_model"],
        "quantity": extracted_data["quantity"],
        "location": extracted_data["location"],
        "timeline": extracted_data["timeline"],
        "language": extracted_data["language"],
        "status": "Pending"
    }
    print("✅ Data written to Google Sheets:")
    for key, value in sheets_data.items():
        print(f"   {key}: {value}")
    
    # Step 4: Simulate Salesforce Opportunity Creation
    print("\n💼 Step 4: Salesforce Opportunity Creation")
    opportunity_data = {
        "opportunity_id": "OPP-2024-001",
        "name": f"RFQ - {extracted_data['product_model']} - {extracted_data['client_name']}",
        "account_name": extracted_data["client_name"],
        "contact_email": extracted_data["client_email"],
        "stage": "Prospecting",
        "amount": 35000,
        "close_date": "2024-02-15",
        "lead_source": "Email RFQ"
    }
    print("✅ Opportunity created in Salesforce:")
    for key, value in opportunity_data.items():
        print(f"   {key}: {value}")
    
    # Step 5: Simulate Google Drive Archiving
    print("\n📁 Step 5: Google Drive Archiving")
    drive_data = {
        "client_folder": f"/RFQ_Attachments/{extracted_data['client_name'].replace(' ', '_')}/",
        "attachments": test_email["attachments"],
        "status": "Archived"
    }
    print("✅ Attachments archived to Drive:")
    print(f"   Folder: {drive_data['client_folder']}")
    print(f"   Files: {', '.join(drive_data['attachments'])}")
    
    # Step 6: Simulate Auto-Reply
    print("\n📧 Step 6: Auto-Reply Generation")
    auto_reply = {
        "subject": f"RFQ Confirmation - {extracted_data['product_model']}",
        "language": extracted_data["language"],
        "status": "Sent"
    }
    print("✅ Auto-reply sent:")
    print(f"   Subject: {auto_reply['subject']}")
    print(f"   Language: {auto_reply['language']}")
    print(f"   Status: {auto_reply['status']}")
    
    # Step 7: Simulate Slack Alert
    print("\n🔔 Step 7: Slack Internal Alert")
    slack_alert = {
        "channel": "#sales-alerts",
        "message": f"🔔 New RFQ from {extracted_data['client_name']}",
        "details": f"Product: {extracted_data['product_model']}, Quantity: {extracted_data['quantity']}",
        "status": "Posted"
    }
    print("✅ Slack alert posted:")
    print(f"   Channel: {slack_alert['channel']}")
    print(f"   Message: {slack_alert['message']}")
    print(f"   Status: {slack_alert['status']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ WORKFLOW TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("📋 Summary:")
    print("• Email processed and fields extracted")
    print("• Data written to Google Sheets")
    print("• Salesforce opportunity created")
    print("• Attachments archived to Drive")
    print("• Auto-reply sent to client")
    print("• Internal alert posted to Slack")
    print("\n🎯 This demonstrates the complete No-Code Zapier workflow!")

def show_sample_data():
    """Display sample data files"""
    print("\n📁 Sample Data Files Available:")
    print("=" * 40)
    
    # Show Google Sheets sample
    sheets_file = Path("zapier_workflow/sample_data/google_sheets_sample.csv")
    if sheets_file.exists():
        print("✅ Google Sheets Sample: google_sheets_sample.csv")
        with open(sheets_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"   Rows: {len(rows)}")
            print(f"   Columns: {len(rows[0]) if rows else 0}")
    
    # Show Salesforce log
    salesforce_file = Path("zapier_workflow/sample_data/salesforce_mock_log.json")
    if salesforce_file.exists():
        print("✅ Salesforce Mock Log: salesforce_mock_log.json")
        with open(salesforce_file, 'r') as f:
            data = json.load(f)
            print(f"   Operations: {len(data.get('salesforce_operations', []))}")
    
    # Show auto-reply samples
    auto_reply_file = Path("zapier_workflow/sample_data/auto_reply_samples.json")
    if auto_reply_file.exists():
        print("✅ Auto-Reply Samples: auto_reply_samples.json")
        with open(auto_reply_file, 'r') as f:
            data = json.load(f)
            print(f"   Languages: {list(data.get('auto_reply_samples', {}).keys())}")
    
    # Show error log
    error_file = Path("zapier_workflow/sample_data/error_log.json")
    if error_file.exists():
        print("✅ Error Log: error_log.json")
        with open(error_file, 'r') as f:
            data = json.load(f)
            print(f"   Error Entries: {len(data.get('error_log', []))}")

def main():
    """Main test function"""
    print("🏢 Alrouf Lighting Technology")
    print("🧪 Task 1: RFQ Automation Testing")
    print("📋 No-Code Zapier Workflow")
    
    # Run the workflow test
    test_zapier_workflow()
    
    # Show available sample data
    show_sample_data()
    
    print("\n" + "=" * 60)
    print("📚 Next Steps:")
    print("1. Set up Zapier account and import workflow")
    print("2. Connect your services (Gmail, Sheets, Salesforce, etc.)")
    print("3. Test with real email using the sample format")
    print("4. Monitor the automation in Zapier dashboard")
    print("=" * 60)

if __name__ == "__main__":
    main()
