# backend/routes/analyze.py
from fastapi import APIRouter, UploadFile, File
from backend.services.mistral_ai import analyze_skin_with_mistral

router = APIRouter()

@router.post("/ai-analyze")
async def ai_analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return analyze_skin_with_mistral(image_bytes)
