import os
import sys
import uvicorn

# Add project root directory to sys.path so backend imports resolve correctly
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the FastAPI application instance from backend/main.py
from backend.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
