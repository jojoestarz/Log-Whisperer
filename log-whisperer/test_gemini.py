#!/usr/bin/env python3
"""Test Gemini API integration with new google-genai package."""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("GEMINI API KEY DIAGNOSTIC")
print("=" * 60)

# Check if .env file exists
import pathlib
env_path = pathlib.Path('.env')
print(f"\n1. Checking .env file...")
print(f"   Location: {env_path.absolute()}")
print(f"   Exists: {env_path.exists()}")

if not env_path.exists():
    print("   ❌ .env file not found!")
    sys.exit(1)

print("\n2. Loading environment variables...")
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
provider = os.getenv("LLM_PROVIDER")

print(f"   LLM_PROVIDER: {provider if provider else '❌ NOT SET'}")
print(f"   GEMINI_API_KEY: ", end="")

if not api_key:
    print("❌ NOT SET")
    print("\n❌ No GEMINI_API_KEY found in .env")
    print("\nTo fix:")
    print("1. Get your API key from: https://aistudio.google.com/app/apikey")
    print("2. Add to .env file:")
    print("   GEMINI_API_KEY=your_actual_key_here")
    sys.exit(1)

if api_key == "your_gemini_api_key_here":
    print("❌ PLACEHOLDER VALUE")
    print("\n❌ GEMINI_API_KEY is still set to placeholder")
    print("\nTo fix:")
    print("1. Get your API key from: https://aistudio.google.com/app/apikey")
    print("2. Replace 'your_gemini_api_key_here' in .env with your actual key")
    sys.exit(1)

print(f"✓ Found ({api_key[:15]}...{api_key[-4:]})")

print("\n3. Testing Gemini SDK installation...")
try:
    from google import genai
    print("   ✓ google-genai package installed")
except ImportError:
    print("   ❌ google-genai package not installed")
    print("\nTo fix:")
    print("   pip install google-genai")
    sys.exit(1)

print("\n4. Configuring Gemini client...")
try:
    client = genai.Client(api_key=api_key)
    print("   ✓ Client configured")
except Exception as e:
    print(f"   ❌ Configuration failed: {e}")
    sys.exit(1)

print("\n5. Testing API connection...")
try:
    response = client.models.generate_content(
        model='models/gemini-2.5-flash',
        contents="Say 'API key works'"
    )
    
    print(f"   ✓ API Response: {response.text.strip()}")
    print("\n✅ GEMINI API KEY IS VALID AND WORKING!")
    
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ API call failed")
    print(f"\nError details: {error_msg}")
    
    if "API_KEY_INVALID" in error_msg or "invalid" in error_msg.lower():
        print("\n❌ The API key is INVALID")
        print("\nPossible reasons:")
        print("- The key was copied incorrectly")
        print("- The key has been revoked")
        print("- The key doesn't have proper permissions")
        print("\nTo fix:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Update GEMINI_API_KEY in .env")
    elif "quota" in error_msg.lower() or "limit" in error_msg.lower() or "429" in error_msg:
        print("\n❌ Rate limit or quota exceeded")
        print("\nFree tier limits:")
        print("- Gemini 2.5 Flash: 15 requests/minute, 1500/day")
        print("- Gemini 2.0 Flash: 15 requests/minute, 1500/day")
        print("\nWait a minute and try again, or use DEMO_MODE=true in .env")
    elif "404" in error_msg or "not found" in error_msg.lower():
        print("\n❌ Model not found")
        print("\nThe model name might be incorrect or not available for your API key.")
        print("Available models: gemini-2.5-flash, gemini-2.0-flash, gemini-2.5-pro")
    else:
        print("\n❌ Unknown error - check your internet connection")
    
    sys.exit(1)

print("\n6. Testing unified LLM client...")
try:
    from llm_client import get_llm_client
    
    client = get_llm_client()
    result = client.create_message(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        system="You are a helpful assistant.",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    
    print(f"   ✓ Unified client response: {result.strip()}")
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - SYSTEM READY!")
    print("=" * 60)
    
except Exception as e:
    print(f"   ❌ Unified client test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
