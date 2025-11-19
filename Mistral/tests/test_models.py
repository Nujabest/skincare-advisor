# tests/test_models.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Analysis

def get_test_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal


def test_can_create_user_and_analysis():
    SessionLocal = get_test_db()
    db = SessionLocal()

    try:
        user = User(age=25, sexe="F", type_peau_habituel="mixte")
        db.add(user)
        db.commit()
        db.refresh(user)

        analysis = Analysis(user_id=user.id, skin_score=75.0)
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        assert user.id is not None
        assert analysis.user_id == user.id

    finally:
        db.close()
