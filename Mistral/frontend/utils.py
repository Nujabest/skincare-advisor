import streamlit as st

def init_session():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
