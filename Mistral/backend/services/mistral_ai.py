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
    "Analyse cette photo de peau et retourne un JSON strict avec les champs suivants : "
    "{skin_score:int, type_peau:str, problemes:list[str], recommandations:list[str], raw_analysis:str}. "
    "Ne mets PAS de texte en dehors du JSON. "
    "Ne mets PAS de ```json. "
    "Réponds uniquement avec le JSON."
)


def clean_json(raw_text: str) -> str:
    """Nettoie un JSON renvoyé dans un bloc markdown ou contenant du bruit."""

    # Retire ```json et ```
    cleaned = re.sub(r"```json|```", "", raw_text).strip()

    # Supprime sauts de lignes inutiles
    cleaned = cleaned.replace("\n", "").replace("\t", "")

    return cleaned


def analyze_skin_with_mistral(image_bytes: bytes) -> dict:
    """Analyse l'image via Mistral Vision."""
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
                        },
                    ],
                }
            ],
        )

        raw_text = response.choices[0].message.content
        cleaned = clean_json(raw_text)

        # Essaye de parser le JSON propre
        try:
            parsed = json.loads(cleaned)
        except Exception:
            parsed = {
                "skin_score": None,
                "type_peau": None,
                "problemes": [],
                "recommandations": [],
                "raw_analysis": raw_text,
            }

        return parsed

    except Exception as e:
        return {
            "skin_score": None,
            "type_peau": None,
            "problemes": [],
            "recommandations": [],
            "raw_analysis": str(e),
        }
