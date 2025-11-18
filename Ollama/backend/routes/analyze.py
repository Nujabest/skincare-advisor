from fastapi import APIRouter, UploadFile, File
from backend.services.ai_skin import analyze_skin_with_ai

router = APIRouter()

@router.post("/ai-analyze")
async def ai_analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = analyze_skin_with_ai(image_bytes)
    return result
