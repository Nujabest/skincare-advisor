import streamlit as st
from utils import init_session

st.set_page_config(page_title="SkinCare Advisor")

init_session()

if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Connexion.py")
else:
    st.switch_page("pages/3_Profil.py")
