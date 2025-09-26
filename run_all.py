#!/usr/bin/env python3
"""
Master script to run all three tasks
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_task(task_name, command):
    """Run a specific task"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {task_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {task_name} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {task_name} failed with error: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return False
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    print("✅ Requirements check passed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        "logs",
        "data",
        "documents",
        "task1_rfq_automation/logs",
        "task2_quotation_service/logs",
        "task3_rag_knowledge/logs",
        "task3_rag_knowledge/data",
        "task3_rag_knowledge/documents"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created successfully")
    return True

def run_task1():
    """Run Task 1: RFQ Automation (No-Code)"""
    print("\n🎯 Task 1: RFQ → CRM Automation (No-Code)")
    print("This is a No-Code solution using Zapier workflow.")
    print("Please follow the setup instructions in task1_rfq_automation/zapier_workflow/README.md")
    
    # Show Zapier workflow information
    print("\n📋 Zapier Workflow Components:")
    print("• Gmail Trigger: New email with RFQ keywords")
    print("• OpenAI Action: Extract structured data")
    print("• Google Sheets: Write RFQ data")
    print("• Salesforce: Create opportunity")
    print("• Google Drive: Archive attachments")
    print("• Gmail: Send auto-reply (AR/EN)")
    print("• Slack: Post internal alert")
    
    print("\n✅ Task 1 setup instructions available in zapier_workflow/README.md")
    return True

def run_task2():
    """Run Task 2: Quotation Service"""
    print("\n🎯 Task 2: Quotation Microservice")
    print("This will start the FastAPI service for quotation generation.")
    
    # Start the FastAPI service in background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "task2_quotation_service.api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        # Wait a bit for service to start
        time.sleep(3)
        
        print("✅ Task 2 - Quotation Service started")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        
        return True
    except Exception as e:
        print(f"❌ Failed to start Task 2: {e}")
        return False

def run_task3():
    """Run Task 3: RAG Knowledge Base"""
    print("\n🎯 Task 3: RAG Knowledge Base")
    print("This will ingest documents and start the Q&A system.")
    
    # Run the RAG system
    return run_task("Task 3 - RAG Knowledge Base", "python task3_rag_knowledge/main.py")

def show_summary():
    """Show project summary"""
    print(f"\n{'='*60}")
    print("📋 ALROUF LIGHTING TECHNOLOGY - PROJECT SUMMARY")
    print(f"{'='*60}")
    
    print("\n🎯 Completed Tasks:")
    print("✅ Task 1: RFQ → CRM Automation")
    print("   - Email processing and field extraction")
    print("   - Google Sheets integration")
    print("   - Salesforce CRM integration")
    print("   - Google Drive archiving")
    print("   - Auto-reply system (AR/EN)")
    print("   - Slack/Teams notifications")
    
    print("\n✅ Task 2: Quotation Microservice")
    print("   - FastAPI-based service")
    print("   - OpenAI integration")
    print("   - Comprehensive pricing logic")
    print("   - Multi-language support")
    print("   - Docker support")
    print("   - Complete test suite")
    
    print("\n✅ Task 3: RAG Knowledge Base")
    print("   - Document ingestion and processing")
    print("   - Vector database (FAISS/Chroma)")
    print("   - Multi-language Q&A (AR/EN)")
    print("   - Source citation")
    print("   - CLI interface")
    
    print("\n📁 Project Structure:")
    print("├── task1_rfq_automation/     # RFQ automation system")
    print("├── task2_quotation_service/  # Quotation microservice")
    print("├── task3_rag_knowledge/      # RAG knowledge base")
    print("├── docs/                     # Documentation")
    print("├── logs/                     # System logs")
    print("└── data/                     # Data storage")
    
    print("\n🔧 Key Features:")
    print("• Mock services for local development")
    print("• Comprehensive error handling")
    print("• Multi-language support (Arabic/English)")
    print("• OpenAI integration")
    print("• Docker support")
    print("• Complete documentation")
    
    print("\n📚 Documentation:")
    print("• README.md - Project overview")
    print("• docs/task1_rfq_automation.md - Task 1 details")
    print("• docs/task2_quotation_service.md - Task 2 details")
    print("• docs/task3_rag_knowledge.md - Task 3 details")
    
    print("\n🚀 Quick Start:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up environment: cp env.example .env")
    print("3. Run individual tasks or use this master script")
    
    print(f"\n{'='*60}")

def main():
    """Main execution function"""
    print("🏢 ALROUF LIGHTING TECHNOLOGY")
    print("📋 Complete Automation System")
    print("🎯 3 Tasks + Deliverables")
    
    # Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        return False
    
    # Setup directories
    if not setup_directories():
        print("❌ Directory setup failed")
        return False
    
    # Show menu
    print(f"\n{'='*60}")
    print("🎯 SELECT TASK TO RUN")
    print(f"{'='*60}")
    print("1. Task 1: RFQ → CRM Automation")
    print("2. Task 2: Quotation Microservice")
    print("3. Task 3: RAG Knowledge Base")
    print("4. Run All Tasks")
    print("5. Show Project Summary")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                run_task1()
            elif choice == "2":
                run_task2()
            elif choice == "3":
                run_task3()
            elif choice == "4":
                print("\n🚀 Running all tasks...")
                run_task1()
                run_task2()
                run_task3()
            elif choice == "5":
                show_summary()
            else:
                print("❌ Invalid choice. Please enter 0-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
