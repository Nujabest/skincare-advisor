import bcrypt
from sqlalchemy.orm import Session
from backend import models, schemas


# ================================
# 🔐 HASH & Vérification PASSWORD
# ================================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ================================
# 👤 CRÉATION UTILISATEUR
# ================================

def create_user(db: Session, user_in: schemas.UserCreate):
    """Créer un nouvel utilisateur avec hash du mot de passe."""

    hashed_pw = hash_password(user_in.password)

    user = models.User(
        email=user_in.email,
        password_hash=hashed_pw,
        age=user_in.age,
        sexe=user_in.sexe,
        type_peau_habituel=user_in.type_peau_habituel,
        sensibilites=user_in.sensibilites,
        routine_actuelle=user_in.routine_actuelle,
        objectifs=user_in.objectifs,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ================================
# 🔑 CONNEXION UTILISATEUR
# ================================

def login_user(db: Session, email: str, password: str):
    """Retourne l’utilisateur si email + password sont valides."""

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


# ================================
# 🔎 GET USER
# ================================

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ================================
# 🔄 UPDATE USER
# ================================

def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    """Met à jour le profil sans toucher email/password."""
    
    user = get_user(db, user_id)
    if not user:
        return None

    # Mise à jour uniquement des champs fournis
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user
