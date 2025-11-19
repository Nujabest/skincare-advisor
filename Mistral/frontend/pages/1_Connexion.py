import streamlit as st
import requests
from utils import init_session

BACKEND_URL = "http://localhost:8000"
st.title("🔐 Connexion Client")

init_session()

id_client = st.number_input("Entrer l’ID client :", min_value=1, step=1)

if st.button("Connexion"):
    r = requests.get(f"{BACKEND_URL}/user/get/{id_client}")
    if r.status_code == 200:
        st.session_state["user_id"] = id_client
        st.success("Connexion réussie 🎉")
        st.switch_page("pages/3_Profil.py")
    else:
        st.error("Client introuvable ❌")

st.divider()

if st.button("Créer un nouveau client"):
    st.switch_page("pages/2_Creer_Profil.py")
