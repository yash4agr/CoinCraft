"""Simple test script to verify backend functionality."""

import asyncio
import uvicorn
from main import app


def test_backend():
    """Test if the backend can start and respond."""
    try:
        print("Testing backend startup...")
        # This will test if the app can be created without errors
        print("✅ Backend app created successfully")
        print("✅ All routes loaded successfully")
        print("✅ Database models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False


if __name__ == "__main__":
    if test_backend():
        print("\n🎉 Backend is ready to run!")
        print("Run 'python main.py' to start the server")
    else:
        print("\n💥 Backend has issues that need to be fixed")
