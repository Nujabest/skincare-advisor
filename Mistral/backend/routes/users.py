from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import schemas, models
from backend.services.db_users import (
    create_user,
    login_user,
    update_user as update_user_service,
    get_user as get_user_service
)

router = APIRouter(prefix="/user", tags=["User"])


# ================================
# 👤 INSCRIPTION
# ================================
@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)
    return user


# ================================
# 🔐 CONNEXION
# ================================
@router.post("/login", response_model=schemas.UserRead)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user = login_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    return user


# ================================
# 🔎 GET USER BY ID
# ================================
@router.get("/get/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


# ================================
# 🔄 UPDATE USER
# ================================
@router.put("/update/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = update_user_service(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


# ================================
# 📋 GET ALL USERS
# ================================
@router.get("/all", response_model=list[schemas.UserRead])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
