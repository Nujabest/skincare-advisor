import streamlit as st
import requests
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

st.title("🧍 Création de compte")

with st.form("register"):
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    age = st.number_input("Âge", 1, 120)
    sexe = st.selectbox("Sexe", ["F", "M"])
    type_peau = st.selectbox("Type de peau", ["sèche", "normale", "mixte", "grasse"])
    sensibilites = st.text_input("Sensibilités")
    routine = st.text_area("Routine actuelle")
    objectifs = st.text_area("Objectifs")

    submit = st.form_submit_button("Créer")

if submit:
    payload = {
        "email": email,
        "password": password,
        "age": age,
        "sexe": sexe,
        "type_peau_habituel": type_peau,
        "sensibilites": sensibilites,
        "routine_actuelle": routine,
        "objectifs": objectifs
    }

    r = requests.post(f"{BACKEND_URL}/user/register", json=payload)

    if r.status_code == 200:
        user = r.json()
        st.session_state["user_id"] = user["id"]
        st.success("Compte créé 🎉")
        st.switch_page("pages/3_Profil.py")
    else:
        st.error("Erreur lors de la création ❌")
