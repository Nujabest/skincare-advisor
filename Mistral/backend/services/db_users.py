from sqlalchemy.orm import Session
from backend import models, schemas

def create_user(db: Session, user_in: schemas.UserCreate):
    user = models.User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None

    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
