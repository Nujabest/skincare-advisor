from fastapi import APIRouter, UploadFile, File
from engine.analyze import analyze_skin   # Import du moteur
import shutil
from pathlib import Path

router = APIRouter()

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # 1. Sauvegarde temporaire de l'image uploadée
    temp_path = Path("temp.jpg")
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Appel du moteur d'analyse
    result = analyze_skin(str(temp_path))

    # 3. Renvoi du résultat
    return {"status": "success", "analysis": result}
