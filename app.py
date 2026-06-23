import streamlit as st
from datetime import datetime, UTC

from services.gemini_client import load_cache, save_cache
from tools.zip_exporter import build_brand_zip

from agents.planner import create_plan
from agents.research import research_brand
from agents.colors import generate_colors
from agents.typography import generate_typography
from agents.copywriter import generate_copy


# =================================================
# CONFIG
# =================================================

st.set_page_config(
    page_title="DesignPilot AI",
    layout="wide"
)

cache = load_cache()

if "selected_project" not in st.session_state:
    st.session_state.selected_project = None


# =================================================
# UI COMPONENT
# =================================================

def render_block(title, content, emoji="⚪"):
    with st.container():

        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:8px;
            ">
                <div style="
                    font-size:14px;
                    font-weight:600;
                ">
                    {emoji} {title}
                </div>
                <div style="
                    width:8px;
                    height:8px;
                    border-radius:50%;
                    background:rgba(255,255,255,0.25);
                "></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                padding: 14px;
                border-radius: 14px;
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                font-size: 13.5px;
                line-height: 1.6;
                white-space: pre-wrap;
            ">
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )


# =================================================
# LAYOUT
# =================================================

left, center, right = st.columns([1.2, 2.5, 1.3])


# =================================================
# LEFT - PROJECTS
# =================================================

with left:
    st.title("📁 Projects")

    if not cache:
        st.info("No projects yet")

    for key in cache.keys():
        if st.button(f"⚡ {key}", key=f"proj_{key}", use_container_width=True):
            st.session_state.selected_project = key


# =================================================
# CENTER - WORKSPACE
# =================================================

with center:
    st.title("AI Workspace")

    selected = st.session_state.selected_project
    project = cache.get(selected) if selected in cache else None


    # =================================================
    # NEW PROJECT FLOW
    # =================================================
    if not project:

        user_input = st.text_area(
            "Describe your brand idea",
            height=120,
            placeholder="e.g. Luxury coffee brand in Porto for remote workers"
        )

        if st.button("Generate Brand System"):

            if not user_input:
                st.error("Please enter a brand idea")
                st.stop()

            key = user_input.strip().lower()

            cache[key] = {
                "meta": {
                    "input": user_input,
                    "created_at": datetime.now(UTC).isoformat(),
                    "updated_at": datetime.now(UTC).isoformat(),
                    "status": "complete"
                },
                "agents": {
                    "planner": create_plan(user_input),
                    "research": research_brand(user_input),
                    "color": generate_colors(user_input),
                    "typography": generate_typography(user_input),
                    "copywriter": generate_copy(user_input)
                }
            }

            save_cache(cache)

            st.session_state.selected_project = key
            st.success("Generated successfully!")
            st.rerun()


    # =================================================
    # PROJECT VIEW
    # =================================================
    else:

        meta = project["meta"]
        agents = project["agents"]

        st.info(f"Resuming: {meta['input']}")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            render_block("Planner", agents.get("planner", ""), "🧠")
            render_block("Colors", agents.get("color", ""), "🎨")

        with col2:
            render_block("Research", agents.get("research", ""), "🔍")
            render_block("Typography", agents.get("typography", ""), "🔤")
            render_block("Copy", agents.get("copywriter", ""), "✍️")


# =================================================
# RIGHT - INSPECTOR
# =================================================

with right:

    st.title("Inspector")

    if project:

        meta = project["meta"]

        st.metric("Status", meta.get("status", "unknown"))

        st.markdown("### Input")
        st.write(meta.get("input"))

        st.markdown("### Created")
        st.write(meta.get("created_at"))

        st.divider()

        zip_data = build_brand_zip(meta["input"])

        st.download_button(
            "📦 Download Brand Kit",
            zip_data,
            file_name="designpilot-brand-kit.zip",
            mime="application/zip",
            use_container_width=True
        )