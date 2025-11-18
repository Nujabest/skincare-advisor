from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de la base PostgreSQL (on ajustera plus tard si besoin)
DATABASE_URL = "postgresql://admin:password@db:5432/skincare"

# Moteur de connexion
engine = create_engine(DATABASE_URL)

# Session (connexion par requête)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()
