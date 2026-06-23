from services.gemini_client import load_cache
from tools.filesystem import save_file


def export_project(user_input: str):

    key = user_input.strip().lower()

    cache = load_cache()

    if key not in cache:
        return "No project found."

    project = cache[key]

    brand_guide = f"""
# Brand Guide

## Colors
{project.get('color', '')}

## Typography
{project.get('typography', '')}

## Copy
{project.get('copywriter', '')}
"""

    save_file("brand-guide.md", brand_guide)

    save_file("colors.json", project.get("color", ""))
    save_file("typography.md", project.get("typography", ""))
    save_file("copy.md", project.get("copywriter", ""))

    return "Export completed successfully."