#!/usr/bin/env python3
"""Quick script to verify Anthropic API key is functional."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_api_key():
    """Test the Anthropic API key with a simple request."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ No ANTHROPIC_API_KEY found in environment", flush=True)
        return False
    
    print(f"✓ API key found: {api_key[:20]}...", flush=True)
    
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        # Make a minimal test request
        print("\nTesting API key with a simple request...", flush=True)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "Say 'API key works'"}
            ]
        )
        
        response_text = message.content[0].text
        print(f"✓ API Response: {response_text}", flush=True)
        print(f"✓ Model: {message.model}", flush=True)
        print(f"✓ Usage: {message.usage.input_tokens} input tokens, {message.usage.output_tokens} output tokens", flush=True)
        print("\n✅ API key is functional!", flush=True)
        return True
        
    except Exception as e:
        print(f"\n❌ API key verification failed: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if verify_api_key() else 1)
