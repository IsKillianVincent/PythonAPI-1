import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@")
API_FALLBACK_URL = os.getenv("API_FALLBACK_URL", "https://currency-api.pages.dev/")
API_VERSION = os.getenv("API_VERSION", "v1")
