import streamlit as st
from datetime import datetime

from agents import create_plan, generate_colors, research_brand, generate_copy, generate_typography

from services.gemini_client import get_cache_metadata

st.title("DesignPilot AI")

user_input = st.text_input("Describe your business idea")

if st.button("Generate Brand System"):
    if user_input:
        col1, col2 = st.columns(2)

        col1.metric("Agents", "5")
        col2.metric("Cache", "Enabled")

        metadata = get_cache_metadata(user_input)

        if metadata and metadata["created_at"]:
            created = datetime.fromisoformat(metadata["created_at"])

            st.caption(
                f"📁 Project created: {created.strftime('%d %B %Y at %H:%M UTC')}"
            )

        st.subheader("Planner Agent")
        st.write(create_plan(user_input))

        st.subheader("Research Agent")
        st.write(research_brand(user_input))

        st.subheader("Color Agent")
        st.write(generate_colors(user_input))

        st.subheader("Typography Agent")
        st.write(generate_typography(user_input))

        st.subheader("Copywriter Agent")
        st.write(generate_copy(user_input))