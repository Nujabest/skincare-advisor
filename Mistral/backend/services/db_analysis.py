from sqlalchemy.orm import Session
from backend import models, schemas


def create_analysis(db: Session, analysis_in: schemas.AnalysisCreate):
    analysis = models.Analysis(**analysis_in.dict())
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

def get_analyses_by_user(db: Session, user_id: int):
    """Retourne toutes les analyses d'un utilisateur, triées de la plus récente à la plus ancienne."""
    return (
        db.query(models.Analysis)
        .filter(models.Analysis.user_id == user_id)
        .order_by(models.Analysis.created_at.desc())
        .all()
    )