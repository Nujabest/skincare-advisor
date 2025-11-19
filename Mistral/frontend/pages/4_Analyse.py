import streamlit as st
import requests
import tempfile
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

# ----------------------------------------------------------
# Vérification connexion
# ----------------------------------------------------------
if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Connexion.py")

uid = st.session_state["user_id"]

st.title("📸 Analyse de peau (IA)")
st.write("Envoyez une photo pour obtenir une analyse complète.")

# ----------------------------------------------------------
# STATE : éviter doubles analyses
# ----------------------------------------------------------
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# ----------------------------------------------------------
# INPUTS : Webcam ou Upload
# ----------------------------------------------------------
webcam_img = st.camera_input("Prendre une photo 📷")
uploaded_img = st.file_uploader("Ou importer une image :", type=["jpg", "jpeg", "png"])

# Stocker l'image dans session_state
if webcam_img:
    st.session_state.image_bytes = webcam_img.getvalue()
elif uploaded_img:
    st.session_state.image_bytes = uploaded_img.getvalue()


# ----------------------------------------------------------
# FONCTION : Envoi image au backend
# ----------------------------------------------------------
def send_image_to_backend():
    if st.session_state.image_bytes is None:
        st.error("Aucune image détectée ❌")
        return

    files = {
        "file": ("photo.jpg", st.session_state.image_bytes, "image/jpeg")
    }

    with st.spinner("Analyse en cours…"):
        r = requests.post(
            f"{BACKEND_URL}/analysis/create/{uid}",
            files=files
        )

    if r.status_code != 200:
        st.error("Erreur lors de l’analyse ❌")
        st.write(r.text)
        return

    data = r.json()

    # Affichage résultats
    st.success("Analyse terminée 🎉")
    st.subheader("🧪 Résultats IA")
    st.write(f"**Score peau :** {data['skin_score']}")
    st.write(f"**Type :** {data['type_peau']}")
    st.write(f"**Problèmes :** {data['problemes']}")
    st.write(f"**Recommandations :** {data['recommandations']}")

    # Rapport premium
    premium = data.get("premium_report")
    if premium:
        st.subheader("💎 Rapport Beauté Premium")
        st.markdown(premium)
    else:
        st.info("Aucun rapport premium n’a été généré.")

    st.session_state.analysis_done = True


# ----------------------------------------------------------
# BOUTON : lancer analyse IA
# ----------------------------------------------------------
if st.button("📊 Lancer l’analyse IA"):
    send_image_to_backend()


# ----------------------------------------------------------
# BOUTON : Heatmap IA (zones problématiques)
# ----------------------------------------------------------
st.write("---")
st.write("### 🔥 Voir zones problématiques")

if st.button("🔥 Générer la heatmap"):
    if st.session_state.image_bytes is None:
        st.error("Aucune photo disponible ❌")
    else:
        with st.spinner("Analyse des zones en cours…"):
            r = requests.post(
                f"{BACKEND_URL}/analysis/heatmap/{uid}",
                files={"file": ("photo.jpg", st.session_state.image_bytes)}
            )

        if r.status_code == 200:
            st.image(r.content, caption="Zones problématiques détectées 🧠")
        else:
            st.error("Impossible de générer la heatmap.")


# ----------------------------------------------------------
# Bouton reset
# ----------------------------------------------------------
st.write("---")
if st.button("🔄 Prendre une nouvelle photo"):
    st.session_state.image_bytes = None
    st.session_state.analysis_done = False
    st.rerun()
