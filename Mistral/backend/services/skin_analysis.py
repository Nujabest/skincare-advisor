import os
import base64
import json
import re
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)

PROMPT = (
    "Analyse cette photo de peau et retourne STRICTEMENT un JSON du format suivant : "
    "{"
    "\"skin_score\": int,"
    "\"type_peau\": \"string\","
    "\"problemes\": [\"string\", ...],"
    "\"recommandations\": [\"string\", ...],"
    "\"raw_analysis\": \"string\""
    "}. "
    "⚠️ IMPORTANT : Retourne uniquement le JSON. AUCUNE explication, AUCUN texte autour, "
    "AUCUN ```json, AUCUNE phrase. Juste le JSON pur."
)

def clean_json(text: str) -> str:
    """Remove ```json or extra text around JSON."""
    text = re.sub(r"```json|```", "", text).strip()
    return text

def analyze_skin(image_bytes: bytes) -> dict:
    """Call Mistral Vision and return extracted JSON."""

    b64 = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                }
            ]
        )

        raw = response.choices[0].message.content
        cleaned = clean_json(raw)

        try:
            parsed = json.loads(cleaned)
            return parsed

        except:
            return {
                "skin_score": None,
                "type_peau": None,
                "problemes": [],
                "recommandations": [],
                "raw_analysis": raw
            }

    except Exception as e:
        return {
            "skin_score": None,
            "type_peau": None,
            "problemes": [],
            "recommandations": [],
            "raw_analysis": f"ERROR: {str(e)}"
        }
