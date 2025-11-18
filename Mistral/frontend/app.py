import streamlit as st
import requests
import tempfile

BACKEND_URL = "http://localhost:8000"

st.title("SkinCare Advisor 💄")

uploaded_file = st.file_uploader("Choisissez une photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Image sélectionnée", width=400)
    st.info("Analyse de la peau en cours… ⏳")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    with open(temp_path, "rb") as f:
        files = {"file": (uploaded_file.name, f, uploaded_file.type)}

        try:
            response = requests.post(f"{BACKEND_URL}/ai-analyze", files=files, timeout=90)
            data = response.json()

            if data["status"] == "success":
                st.success("Analyse terminée !")
                st.markdown(data["raw"])
            else:
                st.error("Erreur : " + data["raw"])

        except Exception as e:
            st.error(f"Impossible de contacter le backend : {e}")

st.write("---")

if st.button("Tester la connexion à Mistral 🧪"):
    r = requests.get(f"{BACKEND_URL}/test-mistral")
    st.json(r.json())
