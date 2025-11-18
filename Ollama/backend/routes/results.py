from fastapi import APIRouter
from backend.services.recommendation_service import get_recommendations  # <-- ICI EN HAUT

router = APIRouter()


@router.get("/results/{analysis_id}")
async def get_results(analysis_id: int):
    return {"analysis_id": analysis_id, "result": "pending"}


@router.get("/recommend/{skin_type}")
async def recommend(skin_type: str):
    return {"recommendations": get_recommendations(skin_type)}
