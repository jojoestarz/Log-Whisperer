from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:20]}...")

client = genai.Client(api_key=api_key)

# Try listing models first
try:
    print("\nListing available models...")
    models = list(client.models.list())
    if models:
        print(f"Found {len(models)} models:")
        for m in models[:5]:
            print(f"  - {m.name}")
        model_to_use = models[0].name
    else:
        print("No models found, using default")
        model_to_use = "models/gemini-2.5-flash"
except Exception as e:
    print(f"Could not list models: {e}")
    model_to_use = "models/gemini-2.5-flash"

print(f"\nUsing model: {model_to_use}")

response = client.models.generate_content(
    model=model_to_use,
    contents="Say hello"
)

print(f"Response: {response.text}")
print("SUCCESS!")
