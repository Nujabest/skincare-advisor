import streamlit as st
import requests
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Connexion.py")

uid = st.session_state["user_id"]

st.title("🕒 Historique des analyses")

r = requests.get(f"{BACKEND_URL}/analysis/user/{uid}")

if r.status_code == 200:
    analyses = r.json()

    if len(analyses) == 0:
        st.info("Aucune analyse encore.")
    else:
        for a in analyses:
            st.write("------")
            st.write(f"📅 **{a['created_at']}**")
            st.write(f"- Score : {a['skin_score']}")
            st.write(f"- Type : {a['type_peau']}")
            st.write(f"- Problèmes : {a['problemes']}")
            st.write(f"- Recommandations : {a['recommandations']}")
else:
    st.error("Erreur chargement historique ❌")
