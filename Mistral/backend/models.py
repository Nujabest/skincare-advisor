from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    sexe = Column(String, nullable=True)
    type_peau_habituel = Column(String, nullable=True)
    sensibilites = Column(String, nullable=True)
    routine_actuelle = Column(String, nullable=True)
    objectifs = Column(String, nullable=True)

    analyses = relationship("Analysis", back_populates="user")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    skin_score = Column(Float, nullable=True)
    type_peau = Column(String, nullable=True)
    problemes = Column(String, nullable=True)
    recommandations = Column(String, nullable=True)
    raw_analysis = Column(String, nullable=True)

    image_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
