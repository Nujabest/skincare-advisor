from sqlalchemy.orm import Session
from backend import models, schemas


def create_analysis(db: Session, analysis_in: schemas.AnalysisCreate):
    analysis = models.Analysis(**analysis_in.dict())
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis
