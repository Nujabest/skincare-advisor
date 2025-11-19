import streamlit as st
import requests
from utils import init_session

BACKEND_URL = "http://localhost:8000"

st.title("🔐 Connexion")

init_session()

# --- Formulaire de connexion ---
st.subheader("Se connecter")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Connexion"):
    payload = {"email": email, "password": password}
    r = requests.post(f"{BACKEND_URL}/user/login", json=payload)

    if r.status_code == 200:
        user = r.json()
        st.session_state["user_id"] = user["id"]
        st.success("Connexion réussie 🎉")
        st.switch_page("pages/3_Profil.py")
    else:
        st.error("Email ou mot de passe incorrect ❌")

st.divider()

# --- Lien vers inscription ---
st.subheader("Créer un compte")
if st.button("Inscription"):
    st.switch_page("pages/2_Creer_Profil.py")
