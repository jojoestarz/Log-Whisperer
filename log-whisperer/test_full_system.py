#!/usr/bin/env python3
"""Test the full system to identify where Anthropic errors come from."""

import sys
import traceback

print("=" * 60)
print("FULL SYSTEM TEST")
print("=" * 60)

# Test 1: Config
print("\n1. Testing config...")
try:
    import config
    print(f"   ✓ LLM_PROVIDER: {config.LLM_PROVIDER}")
    if config.LLM_PROVIDER != "gemini":
        print(f"   ⚠️  WARNING: Provider is not gemini!")
except Exception as e:
    print(f"   ❌ Config error: {e}")
    sys.exit(1)

# Test 2: LLM Client
print("\n2. Testing LLM client...")
try:
    from llm_client import get_llm_client
    client = get_llm_client()
    print(f"   ✓ Client provider: {client.provider.value}")
except Exception as e:
    print(f"   ❌ Client error: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: Decision Agent
print("\n3. Testing decision_agent...")
try:
    from agents import decision_agent
    print(f"   ✓ decision_agent imported")
    # Check if it has any Anthropic imports
    import inspect
    source = inspect.getsource(decision_agent)
    if "from anthropic import" in source or "import anthropic" in source:
        print(f"   ⚠️  WARNING: decision_agent still imports Anthropic directly!")
    else:
        print(f"   ✓ No direct Anthropic imports")
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# Test 4: Writer Agent
print("\n4. Testing writer_agent...")
try:
    from agents import writer_agent
    print(f"   ✓ writer_agent imported")
    import inspect
    source = inspect.getsource(writer_agent)
    if "from anthropic import" in source or "import anthropic" in source:
        print(f"   ⚠️  WARNING: writer_agent still imports Anthropic directly!")
    else:
        print(f"   ✓ No direct Anthropic imports")
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# Test 5: Council Agent
print("\n5. Testing council_agent...")
try:
    from agents import council_agent
    print(f"   ✓ council_agent imported")
    import inspect
    source = inspect.getsource(council_agent)
    if "from anthropic import" in source or "import anthropic" in source:
        print(f"   ⚠️  WARNING: council_agent still imports Anthropic directly!")
    else:
        print(f"   ✓ No direct Anthropic imports")
except Exception as e:
    print(f"   ❌ Error: {e}")
    traceback.print_exc()

# Test 6: Actual API call
print("\n6. Testing actual API call...")
try:
    result = client.create_message(
        model="claude-sonnet-4-20250514",
        max_tokens=20,
        system="You are helpful.",
        messages=[{"role": "user", "content": "Say hi"}]
    )
    print(f"   ✓ API call successful")
    print(f"   ✓ Response: {result.strip()}")
except Exception as e:
    error_str = str(e)
    print(f"   ❌ API call failed: {error_str[:200]}")
    
    if "401" in error_str and "anthropic" in error_str.lower():
        print(f"\n   🔍 DIAGNOSIS:")
        print(f"   This is an Anthropic 401 error, but config says use Gemini.")
        print(f"   Possible causes:")
        print(f"   1. Python is using cached bytecode")
        print(f"   2. Some code is bypassing the unified client")
        print(f"   3. The llm_client is not reading config correctly")
        traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - SYSTEM READY!")
print("=" * 60)
