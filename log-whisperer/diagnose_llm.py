#!/usr/bin/env python3
"""Diagnose which LLM provider is being used."""

print("=" * 60)
print("LLM PROVIDER DIAGNOSTIC")
print("=" * 60)

# Check config
import config
print(f"\n1. Config values:")
print(f"   LLM_PROVIDER: {config.LLM_PROVIDER}")
print(f"   ANTHROPIC_API_KEY: {'Set' if config.ANTHROPIC_API_KEY else 'Not set'}")
print(f"   GEMINI_API_KEY: {'Set' if config.GEMINI_API_KEY else 'Not set'}")

# Check unified client
print(f"\n2. Testing unified LLM client:")
try:
    from llm_client import get_llm_client
    client = get_llm_client()
    print(f"   ✓ Client created")
    print(f"   ✓ Provider: {client.provider.value}")
    
    if client.provider.value == "anthropic":
        print(f"   ⚠️  WARNING: Using Anthropic (invalid key)")
        print(f"   → Change LLM_PROVIDER=gemini in .env")
    elif client.provider.value == "gemini":
        print(f"   ✓ Using Gemini (correct)")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test a simple call
print(f"\n3. Testing actual API call:")
try:
    from llm_client import get_llm_client
    client = get_llm_client()
    
    result = client.create_message(
        model="claude-sonnet-4-20250514",
        max_tokens=20,
        system="You are helpful.",
        messages=[{"role": "user", "content": "Say hi"}]
    )
    
    print(f"   ✓ API call successful")
    print(f"   ✓ Response: {result.strip()}")
    print(f"\n✅ System is using {client.provider.value.upper()} correctly!")
    
except Exception as e:
    error_str = str(e)
    print(f"   ❌ API call failed")
    
    if "401" in error_str or "authentication" in error_str.lower():
        print(f"   ❌ Authentication error - wrong API key")
        if "anthropic" in error_str.lower() or "x-api-key" in error_str.lower():
            print(f"   ⚠️  This is an ANTHROPIC error")
            print(f"   → The system is trying to use Anthropic instead of Gemini")
            print(f"   → Check that LLM_PROVIDER=gemini in .env")
            print(f"   → Clear Python cache: find . -name __pycache__ -exec rm -rf {{}} +")
    elif "429" in error_str or "quota" in error_str.lower():
        print(f"   ⚠️  Rate limit exceeded")
        print(f"   → Wait a minute or set DEMO_MODE=true")
    else:
        print(f"   Error: {error_str[:200]}")

print("\n" + "=" * 60)
