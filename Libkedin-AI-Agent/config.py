import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_MEMBER_ID = os.getenv("LINKEDIN_MEMBER_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LINKEDIN_CODE = os.getenv("LINKEDIN_CODE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")


if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")
