import streamlit as st
import requests
import tempfile

BACKEND_URL = "http://localhost:8000"

st.title("SkinCare Advisor 💄")

# ============================
# ÉTAPE 1 : Formulaire utilisateur
# ============================

st.header("🧍‍♀️ Créer mon profil")

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if st.session_state["user_id"] is None:

    with st.form("create_user_form"):
        age = st.number_input("Âge", min_value=1, max_value=120, step=1)
        sexe = st.selectbox("Sexe", ["F", "M"])
        type_peau_habituel = st.selectbox(
            "Type de peau habituel",
            ["sèche", "normale", "mixte", "grasse", "sensible"]
        )
        sensibilites = st.text_input("Sensibilités connues")
        routine_actuelle = st.text_area("Routine actuelle")
        objectifs = st.text_area("Objectifs (anti-âge, acné, hydratation...)")

        submitted = st.form_submit_button("Créer mon profil")

    if submitted:
        payload = {
            "age": age,
            "sexe": sexe,
            "type_peau_habituel": type_peau_habituel,
            "sensibilites": sensibilites,
            "routine_actuelle": routine_actuelle,
            "objectifs": objectifs
        }

        try:
            resp = requests.post(f"{BACKEND_URL}/user/create", json=payload)
            data = resp.json()

            if resp.status_code == 200:
                st.success(f"Profil créé avec succès ! 🎉 ID = {data['id']}")
                st.session_state["user_id"] = data["id"]
            else:
                st.error(f"Erreur backend : {data}")

        except Exception as e:
            st.error(f"Impossible de contacter le backend : {e}")

# ============================
# ÉTAPE 2 : Analyse IA
# ============================

if st.session_state["user_id"] is None:
    st.warning("Veuillez d’abord créer un profil avant d’analyser votre peau.")
else:
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
                response = requests.post(
                    f"{BACKEND_URL}/analysis/create/{st.session_state['user_id']}",
                    files=files,
                    timeout=90
                )

                data = response.json()

                if response.status_code == 200:
                    st.success("Analyse terminée ! 😍")

                    st.markdown(f"""
                    ### Résultats de l'analyse :
                    - **Score peau** : {data.get("skin_score")}
                    - **Type de peau** : {data.get("type_peau")}
                    - **Problèmes détectés** : {data.get("problemes")}
                    - **Recommandations** : {data.get("recommandations")}
                    """)

                else:
                    st.error("Erreur : " + str(data))

            except Exception as e:
                st.error(f"Impossible de contacter le backend : {e}")

st.write("———")
