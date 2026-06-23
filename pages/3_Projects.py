import streamlit as st
from services.gemini_client import load_cache

st.title("📁 Projects")

cache = load_cache()

if not cache:
    st.info("No projects yet.")
    st.stop()

# store selected project
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None

st.subheader("Your Projects")

for key, project in cache.items():

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"### {key}")
        st.caption(f"Status: {project.get('status', 'unknown')}")

    with col2:
        if st.button("Open", key=key):
            st.session_state.selected_project = key
            st.switch_page("pages/2_Create.py")