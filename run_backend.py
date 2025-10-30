#!/usr/bin/env python3
"""
Script to run the AI Agent Platform backend
"""
import os
import sys
import subprocess

def main():
    print("🤖 Starting AI Agent Platform Backend...")
    print("📍 Backend will run on: http://localhost:5000")
    print("📋 API Documentation: http://localhost:5000/")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        os.chdir(backend_dir)
        
        # Run the Flask app
        subprocess.run([sys.executable, 'app.py'])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()