import streamlit as st

from agents.planner import create_plan
from agents.research import research_brand
from agents.colors import generate_colors
from agents.typography import generate_typography

st.title("DesignPilot AI")

user_input = st.text_input("Describe your business idea")

if st.button("Generate Brand System"):
    if user_input:

     

        st.subheader("Planner Agent")
        st.write(create_plan(user_input))

        st.subheader("Research Agent")
        st.write(research_brand(user_input))

        st.subheader("Color Agent")
        st.write(generate_colors(user_input))

        st.subheader("Typography Agent")
        st.write(generate_typography(user_input))