from fastapi import APIRouter

router = APIRouter()

@router.get("/results/{analysis_id}")
async def get_results(analysis_id: int):
    # Plus tard : récupérer en base
    return {"analysis_id": analysis_id, "result": "pending"}
