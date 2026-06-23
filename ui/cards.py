import streamlit as st
from ui.state import get_status


def agent_card(title: str, content: str, agent_key: str):

    status = get_status(agent_key)

    status_map = {
        "complete": "🟢",
        "thinking": "🟡",
        "idle": "⚪"
    }

    icon = status_map.get(status, "⚪")

    with st.container():

        col1, col2 = st.columns([6, 1])

        with col1:
            st.markdown(f"### {title}")

        with col2:
            st.markdown(icon)

        placeholder = st.empty()

        with placeholder:
            if status == "thinking":
                st.markdown("**Thinking...**")
                st.progress(80)
            elif content:
                st.markdown(
                    f"""
                    <div style="
                        padding:14px;
                        border-radius:12px;
                        background:rgba(255,255,255,0.03);
                        border:1px solid rgba(255,255,255,0.08);
                        font-size:13.5px;
                        line-height:1.6;
                        white-space:pre-wrap;
                    ">
                        {content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown("_Not generated yet_")
                