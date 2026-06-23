import streamlit as st
from services.gemini_client import load_cache
from agents import (
    create_plan, 
    generate_colors, 
    research_brand, 
    generate_copy, 
    generate_typography
)


st.set_page_config(layout="wide")

cache = load_cache()


# -------------------------
# LAYOUT: 3 COLUMNS (FRAMER STYLE)
# -------------------------
left, center, right = st.columns([1.2, 2.5, 1.2])


# =========================
# LEFT: PROJECT LIST
# =========================
with left:
    st.title("Projects")

    if cache:
        for key in cache.keys():
            if st.button(key, key=f"p_{key}"):
                st.session_state.selected_project = key


# =========================
# CENTER: WORKSPACE
# =========================
with center:
    st.title("AI Workspace")

    selected = st.session_state.get("selected_project", None)

    if selected and selected in cache:
        project = cache[selected]
        user_input = project["meta"]["input"]
    else:
        user_input = st.text_input("Describe your brand idea")

    if st.button("Generate") and user_input:

        st.markdown("## Planner")
        st.container(border=True).write(create_plan(user_input))

        st.markdown("## Research")
        st.container(border=True).write(research_brand(user_input))

        st.markdown("## Colors")
        st.container(border=True).write(generate_colors(user_input))

        st.markdown("## Typography")
        st.container(border=True).write(generate_typography(user_input))

        st.markdown("## Copy")
        st.container(border=True).write(generate_copy(user_input))


# =========================
# RIGHT: INSPECTOR PANEL
# =========================
with right:
    st.title("Inspector")

    if selected and selected in cache:
        project = cache[selected]

        st.write("### Status")
        st.info(project.get("status", "unknown"))

        st.write("### Created")
        st.write(project.get("created_at", "N/A"))

        st.write("### Input")
        st.write(project.get("input", ""))

        st.divider()

        if st.button("Export ZIP"):
            from tools.zip_exporter import build_brand_zip
            zip_data = build_brand_zip(selected)

            if zip_data:
                st.download_button(
                    "Download Brand Kit",
                    zip_data,
                    file_name="brand-kit.zip",
                    mime="application/zip"
                )