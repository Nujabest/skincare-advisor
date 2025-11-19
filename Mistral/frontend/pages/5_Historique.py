import streamlit as st
import requests
import pandas as pd
from utils import init_session

BACKEND_URL = "http://localhost:8000"
init_session()

if st.session_state["user_id"] is None:
    st.switch_page("pages/1_Login.py")

uid = st.session_state["user_id"]

st.title("🕒 Historique & Comparaison")

# ==========================================
# 1) RÉCUPÉRER LES ANALYSES
# ==========================================
r = requests.get(f"{BACKEND_URL}/analysis/user/{uid}")

if r.status_code != 200:
    st.error("Erreur chargement historique ❌")
    st.stop()

analyses = r.json()

if len(analyses) == 0:
    st.info("Aucune analyse pour le moment.")
    st.stop()

st.subheader("📸 Vos anciennes analyses")

# ==========================================
# 2) AFFICHAGE LISTE + MINIATURES
# ==========================================
for a in analyses:
    with st.container():
        st.write("----")
        cols = st.columns([1, 3])

        # miniature si image_path existe
        if a["image_path"]:
            try:
                cols[0].image(a["image_path"], use_container_width=True)
            except:
                cols[0].write("Pas d’image")
        else:
            cols[0].write("Pas d’image")

        cols[1].write(f"📅 **{a['created_at']}**")
        cols[1].write(f"⭐ Score : **{a['skin_score']}**")
        cols[1].write(f"Type : {a['type_peau']}")
        cols[1].write(f"Problèmes : {a['problemes']}")



# ==========================================
# 3) COMPARAISON AUTOMATIQUE
# ==========================================
scores = [a["skin_score"] for a in analyses]
dates = [a["created_at"] for a in analyses]

df = pd.DataFrame({"date": dates, "score": scores})
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

st.subheader("📈 Évolution de votre peau")

st.line_chart(df, x="date", y="score")

# ==========================================
# 4) CALCUL D'AMÉLIORATION
# ==========================================
first = df["score"].iloc[0]
last = df["score"].iloc[-1]

difference = last - first
days = (df["date"].iloc[-1] - df["date"].iloc[0]).days

if difference > 0:
    st.success(f"🌟 **Amélioration de +{difference:.1f} points en {days} jours !**")
elif difference < 0:
    st.error(f"⚠️ Baisse de {difference:.1f} points en {days} jours.")
else:
    st.info("Aucune évolution pour le moment.")
