"""
Service IA utilisant Ollama (local, open-source)
"""

import ollama

def analyze_skin_with_ai(image_bytes: bytes) -> dict:
    """
    Analyse une photo de peau via un modèle Vision local (LLava / Llama Vision).
    """

    # 1. Envoie l’image au modèle
    response = ollama.chat(
        model="llava",   # ou llama3.2-vision une fois disponible
        messages=[
            {
                "role": "user",
                "content": "Analyse cette peau et donne type de peau, problèmes visibles et conseils.",
                "images": [image_bytes],   # on envoie l’image brute
            }
        ]
    )

    text = response["message"]["content"]

    # 2. On renvoie juste le texte brut pour le moment
    # (on pourra structurer proprement ensuite)
    return {
        "status": "success",
        "raw": text
    }
