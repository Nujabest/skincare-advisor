import base64
import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)

def analyze_skin_with_mistral(image_bytes: bytes) -> dict:
    """Analyse une image via Mistral Vision (Pixtral)."""

    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    try:
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyse cette photo de peau : type de peau, "
                                "problèmes visibles, sévérité, et conseils personnalisés. "
                                "Réponds clairement en français."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        return {"status": "success", "raw": response.choices[0].message.content}

    except Exception as e:
        return {"status": "error", "raw": str(e)}
