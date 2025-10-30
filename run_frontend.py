#!/usr/bin/env python3
"""
Script to run the AI Agent Platform frontend
"""
import os
import sys
import subprocess

def main():
    print("🎨 Starting AI Agent Platform Frontend...")
    print("📍 Frontend will run on: http://localhost:8501") 
    print("📋 Make sure backend is running on http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        # Change to frontend directory
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        os.chdir(frontend_dir)
        
        # Run the Streamlit app
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()