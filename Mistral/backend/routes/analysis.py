from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import json

from backend.database import get_db
from backend.services.skin_analysis import analyze_skin
from backend.services.db_analysis import create_analysis
from backend.utils.files import save_uploaded_image
import backend.schemas as schemas

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post("/create/{user_id}", response_model=schemas.AnalysisRead)
async def create_analysis_route(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Lire l’image
    image_bytes = await file.read()

    # 2. Sauvegarder l’image
    image_path = save_uploaded_image(file, user_id)

    # 3. Appel IA
    ai = analyze_skin(image_bytes)   # ici AI renvoie déjà un DICT propre
    # EXEMPLE :
    # {
    #  "skin_score": 6,
    #  "type_peau": "mature",
    #  "problemes": ["rides", ...],
    #  "recommandations": ["...", "..."],
    #  "raw_analysis": "texte complet"
    # }

    # 4. Construire l'objet à enregistrer
    analysis_in = schemas.AnalysisCreate(
        user_id=user_id,
        image_path=image_path,
        skin_score=ai.get("skin_score"),
        type_peau=ai.get("type_peau"),
        problemes=",".join(ai.get("problemes", [])),
        recommandations=",".join(ai.get("recommandations", [])),
        raw_analysis=ai.get("raw_analysis")  # <-- ON GARDE LE TEXTE BRUT
    )

    # 5. Enregistrer
    analysis = create_analysis(db, analysis_in)

    return analysis
