import streamlit as st


def render_sidebar(cache):

    st.title("🎨 DesignPilot")

    st.markdown("---")

    if st.button(
        "➕ New Project",
        use_container_width=True
    ):
        st.session_state.selected_project = None
        st.rerun()

    st.markdown("### Recent Projects")

    if not cache:
        st.info("No projects yet.")
        return

    for key in cache.keys():

        project = cache[key]

        status = project.get("meta", {}).get(
            "status",
            "unknown"
        )

        icon = "🟢" if status == "complete" else "⚪"

        if st.button(

            f"{icon} {key.title()}",

            key=f"sidebar_{key}",

            use_container_width=True

        ):

            st.session_state.selected_project = key

            st.rerun()