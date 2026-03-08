#!/usr/bin/env python3
"""Test the unified LLM client with Gemini."""

from llm_client import get_llm_client

print("Testing unified LLM client with Gemini...")
print("=" * 60)

try:
    client = get_llm_client()
    print(f"✓ Client initialized (provider: {client.provider.value})")
    
    result = client.create_message(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        system="You are a helpful assistant.",
        messages=[{"role": "user", "content": "Say hello and confirm you're working"}]
    )
    
    print(f"\n✓ Response received:")
    print(f"  {result.strip()}")
    print("\n" + "=" * 60)
    print("✅ UNIFIED CLIENT WORKING WITH GEMINI!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
