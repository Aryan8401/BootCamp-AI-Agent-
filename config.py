import os

API_KEY = os.environ.get("GROQ_API_KEY", "")
BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Set it as an environment variable "
        "(locally via a .env file, or in your hosting platform's "
        "dashboard/secrets settings) before running the app."
    )