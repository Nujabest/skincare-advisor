from fastapi import APIRouter

router = APIRouter()

@router.post("/analyze")
async def analyze_image():
    # Logique d'analyse à venir
    return {"status": "analysis_started"}
