from services.gemini_client import ask_gemini

def research_brand(user_input):
    """
    Research Agent:
    Pretends to analyze brand direction and style.
    """

    prompt = f"""
    RESEARCH RESULTS

    Brand idea: {user_input}

    Style direction:
    - Modern minimalism
    - Warm premium aesthetic
    - Coffee-house luxury feel

    Inspirations:
    - Blue Bottle Coffee
    - Aesop stores
    - Apple product design

    Keywords:
    - artisan
    - premium
    - calm
    - natural
    """

    return ask_gemini(
        prompt=prompt,
        user_input=user_input,
        agent_type="research"
    )