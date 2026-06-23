import io
import json
import zipfile
from services.gemini_client import load_cache, normalize_user_input


def build_brand_zip(user_input: str):

    key = normalize_user_input(user_input)
    cache = load_cache()

    if key not in cache:
        return None

    project = cache[key]
    agents = project.get("agents", {})

    zip_buffer = io.BytesIO()

    # -------------------------
    # BUILD BRAND GUIDE
    # -------------------------
    brand_guide = f"""
# DesignPilot Brand Kit

## Planner
{agents.get('planner', '')}

## Research
{agents.get('research', '')}

## Colors
{agents.get('color', '')}

## Typography
{agents.get('typography', '')}

## Copy
{agents.get('copywriter', '')}
"""

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        # -------------------------
        # HUMAN READABLE GUIDE
        # -------------------------
        zip_file.writestr("designpilot/brand-guide.md", brand_guide)

        # -------------------------
        # RAW PROJECT DATA
        # -------------------------
        zip_file.writestr(
            "designpilot/project.json",
            json.dumps(project, indent=2, ensure_ascii=False)
        )

        # -------------------------
        # DESIGN TOKENS
        # -------------------------
        design_tokens = {
            "colors": agents.get("color", ""),
            "typography": agents.get("typography", "")
        }

        zip_file.writestr(
            "designpilot/design-tokens.json",
            json.dumps(design_tokens, indent=2, ensure_ascii=False)
        )

        # -------------------------
        # README
        # -------------------------
        readme = f"""
# DesignPilot Brand Kit

## Project
{project.get("input", "")}

## Status
{project.get("status", "")}

## Description
This ZIP contains a complete AI-generated brand system including:
- Brand strategy
- Visual identity
- Copywriting
- Design tokens

Generated automatically by DesignPilot AI.
"""

        zip_file.writestr("designpilot/README.md", readme)

        # -------------------------
        # ASSETS PLACEHOLDER
        # -------------------------
        zip_file.writestr("designpilot/assets/.keep", "")

    zip_buffer.seek(0)
    return zip_buffer.getvalue()