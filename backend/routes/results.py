from fastapi import APIRouter

router = APIRouter()

@router.get("/results/{analysis_id}")
async def get_results(analysis_id: int):
    # Plus tard : récupérer en base
    return {"analysis_id": analysis_id, "result": "pending"}

from backend.services.recommendation_service import get_recommendations

@router.get("/recommend/{skin_type}")
async def recommend(skin_type: str):
    """Retourne les recommandations en fonction du type de peau."""
    return {"recommendations": get_recommendations(skin_type)}
