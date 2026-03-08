#!/usr/bin/env python3
"""Fresh test for Gemini API - no cache issues."""

print("Starting fresh Gemini test...")

# Step 1: Check imports
try:
    from google import genai
    print("✓ google.genai imported successfully")
except ImportError as e:
    print(f"❌ Failed to import: {e}")
    print("Run: pip install google-genai")
    exit(1)

# Step 2: Load API key
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_gemini_api_key_here":
    print("❌ GEMINI_API_KEY not set in .env")
    exit(1)

print(f"✓ API key loaded: {api_key[:15]}...{api_key[-4:]}")

# Step 3: Create client
try:
    client = genai.Client(api_key=api_key)
    print("✓ Client created")
except Exception as e:
    print(f"❌ Client creation failed: {e}")
    exit(1)

# Step 4: Test API call
try:
    print("\nTesting API with models/gemini-2.5-flash...")
    response = client.models.generate_content(
        model='models/gemini-2.5-flash',
        contents="Say hello"
    )
    print(f"✓ Response: {response.text.strip()}")
    print("\n✅ SUCCESS - Gemini is working!")
except Exception as e:
    print(f"❌ API call failed: {e}")
    exit(1)
