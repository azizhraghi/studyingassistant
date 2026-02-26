import subprocess
import time
import os
import sys

def main():
    print("🚀 Starting Atlas Multi-Agent System...")
    
    # Ensure backend directory is in path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # 1. Start FastAPI Backend (Orchestrator)
    print("🧠 Starting Python Orchestrator Backend (localhost:8000)...")
    backend_process = subprocess.Popen(
        ["uvicorn", "backend.api:app", "--reload"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Wait a moment for backend to initialize
    time.sleep(2)

    # 2. Start Streamlit Frontend
    print("🖥️ Starting Streamlit Frontend (localhost:8501)...")
    frontend_process = subprocess.Popen(
        ["streamlit", "run", "app.py"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    try:
        # Keep the script running
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Atlas Multi-Agent System...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
