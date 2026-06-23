import streamlit as st


def init_ui_state():
    if "ui_status" not in st.session_state:
        st.session_state.ui_status = {}


def set_status(agent, status):
    st.session_state.ui_status[agent] = status


def get_status(agent):
    return st.session_state.ui_status.get(agent, "idle")
