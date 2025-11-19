from backend.database import Base, engine
from backend import models

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("OK ✔️")
