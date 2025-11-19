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

st.write("Choisis une méthode pour envoyer ta photo :")

# ----------------------------------------------------------
# OPTION 1 : WEBCAM
# ----------------------------------------------------------
webcam_img = st.camera_input("Prendre une photo avec la webcam 📷")

# ----------------------------------------------------------
# OPTION 2 : UPLOAD MANUEL
# ----------------------------------------------------------
uploaded_img = st.file_uploader("Ou importer une image :", type=["jpg", "jpeg", "png"])

# Boolean pour éviter double envoi
if "sent" not in st.session_state:
    st.session_state.sent = False


def send_image(image_bytes, filename="photo.jpg", mime="image/jpeg"):
    """Envoie l’image au backend + affiche les résultats"""

    files = {"file": (filename, image_bytes, mime)}

    with st.spinner("Analyse en cours…"):
        r = requests.post(f"{BACKEND_URL}/analysis/create/{uid}", files=files)

    if r.status_code != 200:
        st.error("Erreur lors de l’analyse ❌")
        st.write(r.text)
        return

    # récupération de toutes les données
    data = r.json()

    st.success("Analyse terminée 🎉")

    # --- Résultats automatiques ---
    st.subheader("🧪 Résultats IA")
    st.write(f"**Score peau :** {data['skin_score']}")
    st.write(f"**Type :** {data['type_peau']}")
    st.write(f"**Problèmes :** {data['problemes']}")
    st.write(f"**Recommandations :** {data['recommandations']}")

    # --- Rapport premium ---
    premium = data.get("premium_report")

    if premium:
        st.subheader("💎 Rapport Beauté Premium")
        st.markdown(premium)

    else:
        st.info("Aucun rapport premium n’a été généré.")


# ----------------------------------------------------------
# TRAITEMENT : Webcam ou upload
# ----------------------------------------------------------
if webcam_img and not st.session_state.sent:
    st.session_state.sent = True
    send_image(webcam_img.getvalue(), "webcam.jpg")

elif uploaded_img and not st.session_state.sent:
    st.session_state.sent = True
    send_image(uploaded_img.getvalue(), uploaded_img.name, uploaded_img.type)


# bouton reset (permet de reprendre une photo)
if st.button("🔄 Reprendre une autre photo"):
    st.session_state.sent = False
    st.rerun()
