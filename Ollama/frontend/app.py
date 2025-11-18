import streamlit as st
import requests

st.title("SkinCare Advisor")

file = st.file_uploader("Choisissez une photo")

if file:
    with st.spinner("Analyse IA en cours..."):
        files = {"file": file.getvalue()}

        # APPEL A LA ROUTE IA
        response = requests.post("http://localhost:8000/ai-analyze", files=files)

        if response.status_code == 200:
            data = response.json()

            st.subheader("🧠 Résultat IA")
            
            # ⚠️ OLLAMA => on affiche la clé "raw"
            st.write(data.get("raw", "Aucun résultat retourné par l’IA."))

        else:
            st.error("Erreur lors de l'analyse")
