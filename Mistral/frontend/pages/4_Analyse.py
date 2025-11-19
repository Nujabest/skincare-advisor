import streamlit as st
import requests
import tempfile
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Connexion.py")


uid = st.session_state["user_id"]

st.title("📸 Analyse de peau (IA)")

file = st.file_uploader("Choisir une photo", type=["jpg","jpeg","png"])

if file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.getbuffer())
        temp_path = tmp.name

    with open(temp_path, "rb") as f:
        files = {"file": (file.name, f, file.type)}

        with st.spinner("Analyse en cours…"):
            r = requests.post(f"{BACKEND_URL}/analysis/create/{uid}", files=files)

    if r.status_code == 200:
        data = r.json()
        st.success("Analyse terminée 🎉")
        st.write("### Résultats :")
        st.write(f"- **Score peau :** {data['skin_score']}")
        st.write(f"- **Type :** {data['type_peau']}")
        st.write(f"- **Problèmes :** {data['problemes']}")
        st.write(f"- **Recommandations :** {data['recommandations']}")
    else:
        st.error("Erreur d’analyse ❌")
