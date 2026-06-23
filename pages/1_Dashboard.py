import streamlit as st

st.title("📊 Dashboard")

st.metric("Projects", "1")
st.metric("Active AI Agents", "5")

st.divider()

st.subheader("Welcome back 👋")

st.write("""
This is your AI brand system workspace.
Use the sidebar to:
- Create new projects
- View saved projects
- Export brand kits
""")
