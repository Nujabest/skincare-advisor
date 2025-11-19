from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import schemas
from backend.services.skin_analysis import analyze_skin
from backend.services.db_analysis import create_analysis, get_analyses_by_user
from backend.services.db_users import get_user
from backend.services.beauty_report import generate_premium_report

router = APIRouter(prefix="/analysis", tags=["Analysis"])


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

    user = get_user(db, user_id)

    premium_text = generate_premium_report(user, results)

    data = schemas.AnalysisReadWithPremium.model_validate(analysis).model_dump()
    data["premium_report"] = premium_text

    return data


@router.get("/user/{user_id}", response_model=list[schemas.AnalysisRead])
def list_analyses_for_user(user_id: int, db: Session = Depends(get_db)):
    return get_analyses_by_user(db, user_id)
