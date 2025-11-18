from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Pour l'instant on ne fait rien de compliqué
    return {"filename": file.filename}
