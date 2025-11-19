# tests/test_db_users_service.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User
from backend.schemas import UserCreate, UserUpdate
from backend.services import db_users

def get_test_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal

def test_create_and_get_user():
    SessionLocal = get_test_db()
    db = SessionLocal()

    try:
        user_in = UserCreate(age=30, sexe="M", type_peau_habituel="grasse")
        user = db_users.create_user(db, user_in)

        assert isinstance(user, User)
        fetched = db_users.get_user(db, user.id)
        assert fetched.id == user.id

    finally:
        db.close()

def test_update_user():
    SessionLocal = get_test_db()
    db = SessionLocal()

    try:
        user = db_users.create_user(db, UserCreate(age=20))
        updated = db_users.update_user(db, user.id, UserUpdate(age=25))

        assert updated.age == 25

    finally:
        db.close()
