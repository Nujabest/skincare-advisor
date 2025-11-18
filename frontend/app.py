import os
import streamlit as st
import requests

# URL de base de l'API (par défaut en local, override en Docker)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("SkinCare Advisor")

file = st.file_uploader("Choisissez une photo")

if file:
    with st.spinner("Analyse en cours..."):
        files = {"file": file.getvalue()}

        # 1. Appel au backend pour analyser l'image
        response = requests.post(f"{API_URL}/analyze", files=files)

        if response.status_code == 200:
            analysis = response.json()["analysis"]
            st.subheader("🔍 Résultats de l'analyse")
            st.json(analysis)

            # EXTRACTION DES VALEURS
            redness = analysis["redness"]
            brightness = analysis["brightness"]

            # 2. Règle simple pour déterminer le type de peau
            if redness > brightness:
                skin_type = "Dry"
            else:
                skin_type = "Oily"

            st.subheader(f"🧑‍⚕️ Type de peau détecté : **{skin_type}**")

            # 3. Appel de l'API recommandation
            rec_response = requests.get(f"{API_URL}/recommend/{skin_type}")

            if rec_response.status_code == 200:
                recs = rec_response.json()
                st.subheader("💡 Recommandations")
                for item in recs:
                    st.write(f"• {item}")

        else:
            st.error("Erreur lors de l'analyse")
