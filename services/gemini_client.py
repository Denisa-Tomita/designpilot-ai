import os
import json
import re
from dotenv import load_dotenv
from google import genai
from datetime import datetime, UTC

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
CACHE_FILE = "cache.json"

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=API_KEY)


# -------------------------
# CACHE
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
# NORMALIZATION
# -------------------------
def normalize_user_input(user_input: str) -> str:
    user_input = user_input.strip().lower()
    user_input = re.sub(r"\s+", " ", user_input)
    return user_input


# -------------------------
# PROJECT INIT
# -------------------------
def get_or_create_project(cache, key, user_input):
    if key not in cache:
        cache[key] = {
            "meta": {
                "input": user_input,
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": datetime.now(UTC).isoformat(),
                "status": "in_progress"
            },
            "agents": {},
            "exports": {
                "zip_generated": False
            }
        }
    return cache[key]


# =========================================================
# NORMAL GEMINI CALL (FOR EXPORT / CACHE SAFETY)
# =========================================================
def ask_gemini(prompt: str, user_input: str, agent_type: str):

    cache = load_cache()
    key = normalize_user_input(user_input)

    project = get_or_create_project(cache, key, user_input)

    # cache hit
    if agent_type in project["agents"]:
        return project["agents"][agent_type]

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    result = response.text

    project["agents"][agent_type] = result
    project["meta"]["updated_at"] = datetime.now(UTC).isoformat()

    required = ["planner", "research", "color", "typography", "copywriter"]
    if all(a in project["agents"] for a in required):
        project["meta"]["status"] = "complete"

    save_cache(cache)

    return result


# =========================================================
# STREAMING GEMINI CALL (FOR UI ONLY)
# =========================================================
def ask_gemini_stream(prompt: str, user_input: str, agent_type: str):

    cache = load_cache()
    key = normalize_user_input(user_input)

    project = get_or_create_project(cache, key, user_input)

    # cache hit
    if agent_type in project["agents"]:
        yield project["agents"][agent_type]
        return

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        stream=True
    )

    full_text = ""

    for chunk in response:
        if hasattr(chunk, "text"):
            full_text += chunk.text
            yield full_text

    # save final result AFTER streaming
    project["agents"][agent_type] = full_text
    project["meta"]["updated_at"] = datetime.now(UTC).isoformat()

    required = ["planner", "research", "color", "typography", "copywriter"]
    if all(a in project["agents"] for a in required):
        project["meta"]["status"] = "complete"

    save_cache(cache)


# -------------------------
# METADATA
# -------------------------
def get_cache_metadata(user_input: str):
    cache = load_cache()
    key = normalize_user_input(user_input)

    if key not in cache:
        return None

    project = cache[key]

    return {
        "created_at": project["meta"]["created_at"],
        "updated_at": project["meta"]["updated_at"],
        "status": project["meta"]["status"],
        "agents_done": list(project["agents"].keys())
    }


# -------------------------
# OPTIONAL UTILITY
# -------------------------
def save_project(cache, key):
    project = cache[key]

    project["meta"]["updated_at"] = datetime.now(UTC).isoformat()

    required = ["planner", "research", "color", "typography", "copywriter"]
    if all(a in project["agents"] for a in required):
        project["meta"]["status"] = "complete"

    save_cache(cache)