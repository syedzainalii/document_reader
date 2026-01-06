"""
Vercel serverless entry point for FastAPI application.
This file is the entry point for Vercel serverless deployment.
"""
import sys
import os

# Add parent directory to path so we can import from server root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

# Export the FastAPI app for Vercel
handler = app
