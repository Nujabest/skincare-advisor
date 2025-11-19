from fastapi import APIRouter, UploadFile, File, Depends, Response
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import schemas
from backend.services.skin_analysis import analyze_skin
from backend.services.db_analysis import (
    create_analysis,
    get_analyses_by_user
)
from backend.services.db_users import get_user
from backend.services.beauty_report import generate_premium_report

# WOW features
from backend.services.skin_filter import beautify_image
from backend.services.heatmap import add_heatmap
from backend.services.gamification import compute_badges, compute_progression


router = APIRouter(prefix="/analysis", tags=["Analysis"])


# ---------------------------------------------------------
# 1) Analyse et PREMIUM REPORT
# ---------------------------------------------------------
@router.post("/create/{user_id}", response_model=schemas.AnalysisReadWithPremium)
async def create_analysis_route(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = await file.read()

    results = analyze_skin(image_bytes)

    analysis_in = schemas.AnalysisCreate(
        user_id=user_id,
        image_path="placeholder.jpg",
        skin_score=results.get("skin_score"),
        type_peau=results.get("type_peau"),
        problemes=",".join(results.get("problemes", [])),
        recommandations=",".join(results.get("recommandations", [])),
        raw_analysis=results.get("raw_analysis")
    )

    analysis = create_analysis(db, analysis_in)

    # profil utilisateur
    user = get_user(db, user_id)

    # génération du texte premium
    premium_text = generate_premium_report(user, results)

    # réponse enrichie
    data = schemas.AnalysisReadWithPremium.model_validate(analysis).model_dump()
    data["premium_report"] = premium_text

    return data


# ---------------------------------------------------------
# 2) Liste analyses d'un user
# ---------------------------------------------------------
@router.get("/user/{user_id}", response_model=list[schemas.AnalysisRead])
def list_analyses_for_user(user_id: int, db: Session = Depends(get_db)):
    return get_analyses_by_user(db, user_id)


# ---------------------------------------------------------
# 3) Filtre photo "Beautify"
# ---------------------------------------------------------
@router.post("/beautify/{user_id}")
async def beautify_route(
    user_id: int,
    file: UploadFile = File(...)
):
    img_bytes = await file.read()
    result = beautify_image(img_bytes)
    return Response(content=result, media_type="image/jpeg")


# ---------------------------------------------------------
# 4) Heatmap zones problématiques (🔥 FIXED)
# ---------------------------------------------------------
@router.post("/heatmap/{user_id}")
async def heatmap_route(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    img_bytes = await file.read()

    # Récup dernières analyses
    analyses = get_analyses_by_user(db, user_id)
    if not analyses:
        return {"error": "Aucune analyse trouvée pour cet utilisateur."}

    last = analyses[-1]

    detected = (last.problemes or "").split(",")

    result = add_heatmap(img_bytes, detected)
    return Response(content=result, media_type="image/jpeg")


# ---------------------------------------------------------
@router.get("/gamification/{user_id}")
def gamification_route(user_id: int, db: Session = Depends(get_db)):
    analyses = get_analyses_by_user(db, user_id)
    badges, prog = compute_badges(analyses)
    return {"badges": badges, "progression": prog}


