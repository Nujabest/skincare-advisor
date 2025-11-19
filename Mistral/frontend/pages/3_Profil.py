import streamlit as st
import requests
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Connexion.py")

uid = st.session_state["user_id"]

st.title("👤 Profil du client")

r = requests.get(f"{BACKEND_URL}/user/get/{uid}")
user = r.json()

st.write(f"**Âge :** {user['age']}")
st.write(f"**Sexe :** {user['sexe']}")
st.write(f"**Type de peau habituel :** {user['type_peau_habituel']}")
st.write(f"**Sensibilités :** {user['sensibilites']}")
st.write(f"**Routine :** {user['routine_actuelle']}")
st.write(f"**Objectifs :** {user['objectifs']}")



if st.button("Aller à analyse IA ➡️"):
    st.switch_page("pages/4_Analyse.py")

if st.button("Voir l’historique 🕒"):
    st.switch_page("pages/5_Historique.py")

st.button("Se déconnecter 🔐", on_click=lambda: (
    st.session_state.update({"user_id": None}),
    st.switch_page("pages/1_Connexion.py")
))

import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"
uid = st.session_state["user_id"]



r = requests.get(f"{BACKEND_URL}/analysis/gamification/{uid}")
data = r.json()


# --- Gamification ---
g = requests.get(f"{BACKEND_URL}/analysis/gamification/{uid}").json()

if g["progression"]:
    st.success(f"💹 Amélioration : **+{g['progression']}%**")

if g["badges"]:
    st.subheader("🏆 Vos badges")
    for b in g["badges"]:
        st.write(b)
