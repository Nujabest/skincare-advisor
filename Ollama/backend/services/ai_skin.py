"""
Service IA utilisant Ollama (local, open-source)
"""

import ollama

def analyze_skin_with_ai(image_bytes: bytes) -> dict:
    """
    Analyse une photo de peau via un modèle Vision local (LLava / Llama Vision),
    et renvoie une réponse clairement structurée en FRANÇAIS.
    """

    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": (
                    "Tu es un expert en dermatologie. "
                    "Analyse cette photo de peau et répond STRICTEMENT en français. "
                    "Donne :\n"
                    "1) Le type de peau (sèche, grasse, mixte, normale)\n"
                    "2) Les problèmes visibles (acné, rougeurs, taches, rides…)\n"
                    "3) Un diagnostic court\n"
                    "4) Une routine skin care adaptée (matin + soir)\n\n"
                    "Sois précis mais simple à comprendre."
                ),
                "images": [image_bytes]
            }
        ]
    )

    text = response["message"]["content"]

    return {
        "status": "success",
        "raw": text
    }
