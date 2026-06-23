from services.gemini_client import ask_gemini


def generate_colors(user_input):
    prompt = f"""
You are a senior brand designer.

Create a professional color palette for this project:
{user_input}

Return:
- Primary color (hex + name)
- Secondary color (hex + name)
- Accent color (hex + name)
- Background color (hex + name)
- Short explanation of why these colors fit

Make it modern, usable in web design, and consistent with UI/UX best practices.
"""

    return ask_gemini(
        prompt=prompt,
        user_input=user_input,
        agent_type="color"
    )