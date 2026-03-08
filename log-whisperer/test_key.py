import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"Key found: {api_key[:25]}..." if api_key else "No key")

client = Anthropic(api_key=api_key)
msg = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=10,
    messages=[{"role": "user", "content": "Hi"}]
)
print(f"Response: {msg.content[0].text}")
print("API key works!")
