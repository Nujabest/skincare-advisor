from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# ================================
# USER SCHEMAS
# ================================

class UserBase(BaseModel):
    age: Optional[int] = None
    sexe: Optional[str] = None
    type_peau_habituel: Optional[str] = None
    sensibilites: Optional[str] = None
    routine_actuelle: Optional[str] = None
    objectifs: Optional[str] = None


class UserCreate(UserBase):
    # Champs obligatoires pour créer un compte
    email: str
    password: str


class UserLogin(BaseModel):
    # Pour la connexion
    email: str
    password: str


class UserUpdate(UserBase):
    # Mise à jour du profil (email/password non modifiés ici)
    pass


class UserRead(UserBase):
    # Ce qu'on renvoie au frontend
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# ================================
# ANALYSIS SCHEMAS
# ================================

class AnalysisBase(BaseModel):
    skin_score: Optional[float] = None
    type_peau: Optional[str] = None
    problemes: Optional[str] = None   # Liste sous forme de string "acné, taches"
    recommandations: Optional[str] = None
    raw_analysis: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    user_id: int
    image_path: str


class AnalysisRead(AnalysisBase):
    id: int
    user_id: int
    image_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnalysisReadWithPremium(AnalysisRead):
    premium_report: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


