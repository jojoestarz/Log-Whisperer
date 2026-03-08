"""Central config — reads from .env"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# App Configuration
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
ARGO_MOCK = os.getenv("ARGO_MOCK", "true").lower() == "true"
RERUN_APP_ID = os.getenv("RERUN_APP_ID", "log_whisperer")
MODEL = "claude-sonnet-4-20250514"

