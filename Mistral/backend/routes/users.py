from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import schemas
from backend.services import db_users

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create", response_model=schemas.UserRead)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db_users.create_user(db, user_in)
    return user


@router.get("/get/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db_users.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


@router.put("/update/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db_users.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user
