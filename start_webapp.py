#!/usr/bin/env python3
"""
Start React Web Application for Alrouf AI Solutions
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
        return False

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm version: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def install_dependencies():
    """Install React app dependencies"""
    webapp_dir = Path(__file__).parent / "webapp"
    
    if not webapp_dir.exists():
        print("❌ Webapp directory not found")
        return False
    
    print("📦 Installing React app dependencies...")
    try:
        result = subprocess.run(['npm', 'install'], cwd=webapp_dir, check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_react_app():
    """Start the React development server"""
    webapp_dir = Path(__file__).parent / "webapp"
    
    print("🚀 Starting React development server...")
    print("📱 Webapp will be available at: http://localhost:3000")
    print("🔧 Backend services should be running on: http://localhost:8000")
    print()
    print("⚠️  Make sure to start the backend services first:")
    print("   Task 2: uvicorn task2_quotation_service.api.main:app --reload")
    print("   Task 3: python task3_rag_knowledge/main.py")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the React app
        subprocess.run(['npm', 'start'], cwd=webapp_dir)
    except KeyboardInterrupt:
        print("\n🛑 React app stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start React app: {e}")

def main():
    """Main function"""
    print("🌐 Alrouf Lighting Technology - React Web Application")
    print("=" * 60)
    
    # Check prerequisites
    if not check_node_installed():
        sys.exit(1)
    
    if not check_npm_installed():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start React app
    start_react_app()

if __name__ == "__main__":
    main()
