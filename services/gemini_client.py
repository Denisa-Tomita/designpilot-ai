import os
import json
import re
from dotenv import load_dotenv
from google import genai
from datetime import datetime, UTC

# ALWAYS load .env first
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
CACHE_FILE = "cache.json"

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=API_KEY)


# -------------------------
# CACHE UTILITIES
# -------------------------

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


# -------------------------
# PROMPT NORMALIZATION
# -------------------------

def normalize_user_input(user_input: str) -> str:
    user_input = user_input.strip().lower()
    user_input = re.sub(r"\s+", " ", user_input)
    return user_input

def get_cache_metadata(user_input: str):
    cache = load_cache()

    normalized_input = normalize_user_input(user_input)

    if normalized_input not in cache:
        return None

    return {
        "created_at": cache[normalized_input].get("created_at")
    }

# -------------------------
# GEMINI CALL (WITH CACHE)
# -------------------------

def ask_gemini(prompt: str, user_input: str, agent_type: str):

    cache = load_cache()

    normalized_input = normalize_user_input(user_input)

    # Create project entry
    if normalized_input not in cache:
        cache[normalized_input] = {
            "created_at": datetime.now(UTC).isoformat()
        }

    # Cache hit
    if agent_type in cache[normalized_input]:
        print(f"⚡ Cache hit ({agent_type})")
        return cache[normalized_input][agent_type]

    # Gemini call
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    result = response.text

    # Store result
    cache[normalized_input][agent_type] = result

    save_cache(cache)

    return result