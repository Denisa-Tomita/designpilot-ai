from services.gemini_client import ask_gemini

def create_plan(user_input):
    prompt = f"""
    AI DESIGN PLAN

    Project: {user_input}

    1. Research brand style and competitors
    2. Choose typography pairing
    3. Define color palette
    4. Design homepage layout
    5. Write hero section copy
    6. Export final brand system
    """

    return ask_gemini(
        prompt=prompt,
        user_input=user_input,
        agent_type="planner"
    )
