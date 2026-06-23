from services.gemini_client import ask_gemini

def generate_copy(user_input):
    """
    Copywriter Agent

    Creates simple marketing text for a landing page.
    """

    prompt = f"""
    HERO TITLE

    Exceptional {user_input},
    Crafted for Everyday Moments.

    HERO SUBTITLE

    Beautiful design, premium quality,
    and an unforgettable experience.

    CALL TO ACTION

    Explore the Collection
    """

    return ask_gemini(
        prompt=prompt,
        user_input=user_input,
        agent_type="copywriter"
    )