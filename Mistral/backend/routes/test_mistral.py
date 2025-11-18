from fastapi import APIRouter
from mistralai import Mistral
import os

router = APIRouter()

@router.get("/test-mistral")
def test_mistral():
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Dis-moi bonjour en français !"}],
        )

        return {
            "status": "success",
            "response": response.choices[0].message.content,
        }

    except Exception as e:
        return {"status": "error", "raw": str(e)}
