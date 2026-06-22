def generate_typography(user_input):
    """
    Typography Agent

    Chooses a font pairing based on the project.
    """

    typography = f"""
    TYPOGRAPHY SYSTEM

    Project:
    {user_input}

    Heading Font:
    Cormorant Garamond

    Body Font:
    Inter

    Style Notes:

    - Elegant
    - Premium
    - Editorial
    - Easy to read

    Reason:

    The serif heading creates luxury while
    the sans-serif body improves readability.
    """

    return typography