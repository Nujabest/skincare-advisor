import os
import uuid
import base64
import sqlite3
import requests
import json
import re
from datetime import datetime
from dotenv import load_dotenv

from flask import (
    Flask, render_template, request, jsonify, redirect, session,send_from_directory, abort)

from werkzeug.utils import secure_filename


# .ENV
load_dotenv(override=True)



# CONFIG
# API Key
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()

# Model used
MISTRAL_VLM_MODEL = os.getenv("MISTRAL_VLM_MODEL", "pixtral-12b-2409").strip()

# URL API Mistral
MISTRAL_BASE = "https://api.mistral.ai/v1"

#Default Login:1 Password:1
DEMO_LOGIN = os.getenv("DEMO_LOGIN", "1")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "1")



# FLASK

app = Flask(__name__)

# Secret_key pour les sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret")

# HTTPS render
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False



# UPLOADS

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp"}

MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}



# BD

# Fichier de base de données local
DB_PATH = os.path.join(os.path.dirname(__file__), "skinalyze.db")


def db():
    """
    Ouvre une connexion SQLite.
    row_factory permet de lire les colonnes comme un dictionnaire.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Crée la table si elle n'existe pas.
    Ajoute la colonne metrics_json si besoin (migration simple).
    """
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            image_filename TEXT NOT NULL,
            note TEXT,
            diagnostic TEXT NOT NULL
        )
    """)
    conn.commit()

    # Vérifie les colonnes existantes
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(chats)").fetchall()]
    if "metrics_json" not in cols:
        conn.execute("ALTER TABLE chats ADD COLUMN metrics_json TEXT")
        conn.commit()

    conn.close()


def list_chats(limit=200):
    """
    Retourne une liste d'analyses pour la page historique.
    """
    conn = db()
    rows = conn.execute(
        "SELECT id, created_at, image_filename, note FROM chats ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return rows


def get_chat(chat_id: int):
    """
    Récupère une analyse spécifique par ID.
    """
    conn = db()
    row = conn.execute(
        "SELECT id, created_at, image_filename, note, diagnostic, metrics_json FROM chats WHERE id=?",
        (chat_id,)
    ).fetchone()
    conn.close()
    return row


def insert_chat(image_filename: str, note: str, diagnostic: str, metrics_json: str | None) -> int:
    """
    Enregistre une nouvelle analyse dans la DB.
    """
    conn = db()
    cur = conn.execute(
        "INSERT INTO chats (created_at, image_filename, note, diagnostic, metrics_json) VALUES (?, ?, ?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), image_filename, note, diagnostic, metrics_json)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def delete_chat(chat_id: int):
    """
    Supprime une analyse et le fichier image associé.
    """
    row = get_chat(chat_id)
    if not row:
        return

    img = row["image_filename"]

    # Supprime dans la DB
    conn = db()
    conn.execute("DELETE FROM chats WHERE id=?", (chat_id,))
    conn.commit()
    conn.close()

    try:
        path = os.path.join(UPLOAD_DIR, img)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def clear_history():
    """
    Supprime tout l'historique (DB) et toutes les images (uploads).
    """
    rows = list_chats(limit=5000)

    # Vide la DB
    conn = db()
    conn.execute("DELETE FROM chats")
    conn.commit()
    conn.close()

    # Supprime tous les fichiers
    for r in rows:
        try:
            path = os.path.join(UPLOAD_DIR, r["image_filename"])
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass


# DB
init_db()



# Useful functions

def allowed_file(filename: str) -> bool:
    """
    Vérifie l'extension du fichier upload.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def file_to_data_uri(path: str) -> str:
    """
    Convertit une image locale en data URI base64.
    API Mistral accepte une image via URL/data URI.
    """
    ext = os.path.splitext(path)[1].lower()
    mime = MIME_MAP.get(ext, "image/jpeg")

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{b64}"


def strip_think(text: str) -> str:
    """
    Certains modèles peuvent renvoyer <think>...</think>.
    Ici on nettoie pour ne garder que le texte final.
    """
    if not text:
        return ""
    idx = text.find("</think>")
    if idx != -1:
        text = text[idx + len("</think>"):]
    return text.replace("<think>", "").replace("</think>", "").strip()


def extract_metrics_and_text(model_text: str):
    """
    On attend une première ligne du type :
    METRICS: {...json...}

    La fonction retourne :
    - metrics (dict ou None)
    - clean_text (texte à afficher)
    """
    if not model_text:
        return None, ""

    lines = model_text.strip().splitlines()
    first = (lines[0] if lines else "").strip()

    metrics = None
    rest_lines = lines

    if first.startswith("METRICS:"):
        raw = first[len("METRICS:"):].strip()
        try:
            metrics = json.loads(raw)
            rest_lines = lines[1:]
        except Exception:
            metrics = None
            rest_lines = lines

    text = "\n".join(rest_lines).strip()

    # Si markdown, on les supprime
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = text.replace("**", "").replace("```", "")
    return metrics, text


def normalize_metrics(m):
    """
    Assure qu'on a toujours les 6 métriques attendues (pour l'affichage).
    Si le modèle oublie une clé, on met une valeur par défaut.
    """
    defaults = {
        "urgence": "faible",
        "score_peau": 50,
        "confiance": "moyenne",
        "inflammation": "moyenne",
        "acne": "légère",
        "risque_irritation": "moyen"
    }
    if not isinstance(m, dict):
        return defaults

    out = defaults.copy()
    for k in out.keys():
        if k in m and m[k] not in (None, ""):
            out[k] = m[k]
    return out



# AUTHENTIFI

@app.before_request
def require_login():
    """
    Ce hook s'exécute avant chaque requête.
    Si l'utilisateur n'est pas connecté, il est redirigé vers /login.
    On laisse passer static et uploads pour afficher les fichiers.
    """
    if request.path.startswith("/static"):
        return
    if request.path.startswith("/uploads"):
        return
    if request.path in ("/login",):
        return
    if not session.get("logged_in"):
        return redirect("/login")



# in/out

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Page de connexion.
    - GET : affiche le formulaire
    - POST : vérifie identifiants .env
    """
    error = None
    if request.method == "POST":
        login_val = request.form.get("login", "")
        password_val = request.form.get("password", "")

        # Vérification simple des identifiants
        if login_val == DEMO_LOGIN and password_val == DEMO_PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        else:
            error = "Identifiants incorrects"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """
    Déconnexion : on vide la session.
    """
    session.clear()
    return redirect("/login")



@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """
    Permet d'accéder à une image uploadée via /uploads/<filename>.
    """
    return send_from_directory(UPLOAD_DIR, filename)


# emplates

@app.route("/")
def home():
    """
    Page d'accueil.
    """
    return render_template("landing.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload d'une image + note.
    - POST : enregistre le fichier + stocke temporairement en session
    - GET : affiche le formulaire
    """
    if request.method == "POST":
        file = request.files.get("image")
        note = (request.form.get("note") or "").strip()

        if not file or file.filename == "":
            return render_template("upload.html", error="Veuillez ajouter une image.", note=note)

        # Vérifie le format
        if not allowed_file(file.filename):
            return render_template("upload.html", error="Format invalide (png/jpg/jpeg/webp).", note=note)

        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")

        path = os.path.join(UPLOAD_DIR, filename)
        file.save(path)

        # Stocke en session pour l'étape d'analyse
        session["uploaded_image"] = filename
        session["uploaded_note"] = note

        # Redirige vers page "processing"
        return redirect("/processing")

    return render_template("upload.html")


@app.route("/processing")
def processing():
    """
    Page intermédiaire (loader).
    Le front appelle ensuite /api/analyze.
    """
    return render_template("processing.html")


@app.route("/result")
def result():
    """
    Affiche le dernier résultat.
    On essaie d'abord de récupérer depuis la DB via last_chat_id.
    Sinon on fallback sur ce qui est stocké dans la session.
    """
    last_id = session.get("last_chat_id")
    if last_id:
        chat = get_chat(int(last_id))
        if chat:
            # Charge et normalise les métriques
            metrics = None
            try:
                metrics = json.loads(chat["metrics_json"]) if chat["metrics_json"] else None
            except Exception:
                metrics = None
            metrics = normalize_metrics(metrics)

            return render_template("result.html", chat=chat, metrics=metrics, diagnostic=None)

    # Fallback si pas d'id ou pas de chat trouvé
    diagnostic = session.get("last_diagnostic") or "Aucun diagnostic généré."
    metrics = normalize_metrics(session.get("last_metrics"))
    return render_template("result.html", chat=None, metrics=metrics, diagnostic=diagnostic)



# History

@app.route("/history")
def history():
    """
    Liste de toutes les analyses saved.
    """
    return render_template("history.html", chats=list_chats())


@app.route("/chat/<int:chat_id>")
def chat_view(chat_id: int):
    """
    Ouvre une analyse spécifique.
    """
    chat = get_chat(chat_id)
    if not chat:
        abort(404)

    session["last_chat_id"] = chat_id

    # Charge les metrics JSON
    metrics = None
    try:
        metrics = json.loads(chat["metrics_json"]) if chat["metrics_json"] else None
    except Exception:
        metrics = None
    metrics = normalize_metrics(metrics)

    return render_template("result.html", chat=chat, metrics=metrics, diagnostic=None)


@app.route("/chat/<int:chat_id>/delete", methods=["POST"])
def chat_delete(chat_id: int):
    """
    Supprime une analyse depuis history.
    """
    delete_chat(chat_id)

    # Si on a supprimé le "dernier chat", on l'oublie
    if session.get("last_chat_id") == chat_id:
        session.pop("last_chat_id", None)

    return redirect("/history")


@app.route("/history/clear", methods=["POST"])
def history_clear():
    """
    Supprime tout history.
    """
    clear_history()
    session.pop("last_chat_id", None)
    return redirect("/history")


# MISTRAL

def mistral_vision_chat(data_uri: str, user_text: str) -> str:
    """
    Envoie l'image (data_uri) + texte utilisateur à l'API Mistral.
    Le prompt impose un format strict : première ligne METRICS: {...}
    """
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY missing in .env")

    url = f"{MISTRAL_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    # Prompt système
    system_prompt = (
        "Tu es un assistant de soin de la peau (informatif, pas médical). "
        "Tu analyses une PHOTO + le TEXTE utilisateur. "
        "Tu dois être prudent : pas de diagnostic certain, pas de prescription, pas de médicaments sur ordonnance.\n\n"
        "FORMAT OBLIGATOIRE DE SORTIE :\n"
        "- La PREMIÈRE ligne doit être exactement :\n"
        "METRICS: <JSON>\n"
        "où <JSON> est un JSON valide sur une seule ligne avec les clés EXACTES :\n"
        "{"
        "\"urgence\":\"faible|moyenne|élevée\","
        "\"score_peau\":0-100,"
        "\"confiance\":\"faible|moyenne|élevée\","
        "\"inflammation\":\"faible|moyenne|élevée\","
        "\"acne\":\"aucune|légère|modérée|sévère\","
        "\"risque_irritation\":\"faible|moyen|élevé\""
        "}\n\n"
        "- Après cette première ligne, écris un texte PROPRE sans symboles type ###, sans markdown.\n"
        "- Utilise seulement des titres simples en MAJUSCULES + paragraphes bien redigé.\n"
        "- si necessaire listes autorisées uniquement avec des tirets '-'.\n\n"
        "CONTENU ATTENDU :\n"
        "DIAGNOSTIC PROBABLE (avec prudence)\n"
        "TYPE DE PEAU\n"
        "PROBLÈMES DÉTECTÉS\n"
        "ROUTINE RECOMMANDÉE (MATIN / SOIR) avec PRODUITS + MARQUES (2-4 options par étape)\n"
        "COMPLÉMENTS ALIMENTAIRES (optionnel) : 2-3 propositions + raisons + précautions\n"
        "ALIMENTATION : aliments à privilégier + à limiter\n"
        "CONSEILS & PRÉCAUTIONS : 8-12 conseils concrets\n"
        "QUAND CONSULTER : 4 critères concrets\n\n"
        "Si la photo est floue ou insuffisante, indique-le et mets confiance=faible."
    )

    # Si l'utilisateur n'a rien écrit texte par défaut
    if not (user_text or "").strip():
        user_text = "Analyse la photo et donne un rapport de soin de peau. Ajoute des produits avec marques."

    # Payload demandé
    payload = {
        "model": MISTRAL_VLM_MODEL,
        "temperature": 0.5,      # faible = réponses plus stables
        "max_tokens": 2000,      # taille max de réponse
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ]},
        ],
    }

    r = requests.post(url, headers=headers, json=payload, timeout=90)

    # Si erreur API, on renvoie une exception
    if r.status_code != 200:
        raise RuntimeError(f"Mistral error {r.status_code}: {r.text[:400]}")

    data = r.json()
    return data["choices"][0]["message"]["content"].strip()


# API

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Endpoint appelé après l'upload.
    Il récupère l'image en session, appelle Mistral,
    extrait metrics + texte, enregistre dans la DB, puis répond JSON.
    """
    filename = session.get("uploaded_image")
    note = session.get("uploaded_note", "")

    # Vérifie qu'on a  une image dans la session
    if not filename:
        session["last_diagnostic"] = "Erreur: aucune image fournie."
        return jsonify({"error": "No image uploaded"}), 400

    path = os.path.join(UPLOAD_DIR, filename)

    # Vérifie que le fichier existe
    if not os.path.exists(path):
        session["last_diagnostic"] = "Erreur: fichier image introuvable."
        return jsonify({"error": "Image file missing"}), 400

    try:
        data_uri = file_to_data_uri(path)

        reply = mistral_vision_chat(data_uri=data_uri, user_text=note)

        # On supprome <think> si il y a
        reply = strip_think(reply)

        # Extraction du JSON METRICS + texte final
        metrics, clean_text = extract_metrics_and_text(reply)

        # Normalise pour ne jamais ruiner l'affichage
        metrics = normalize_metrics(metrics)

        session["last_diagnostic"] = clean_text
        session["last_metrics"] = metrics

        # Stockage des metrics dans la DB en JSON
        metrics_json = json.dumps(metrics, ensure_ascii=False)

        # Enregistre en DB (image + note + diagnostic + metrics)
        new_id = insert_chat(filename, note, clean_text, metrics_json)
        session["last_chat_id"] = new_id

        return jsonify({"ok": True})

    except Exception as e:
        session["last_diagnostic"] = f"Erreur: {str(e)}"
        session["last_metrics"] = normalize_metrics(None)
        return jsonify({"error": str(e)}), 500


# RUN

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
