from backend.db import Base, engine
from backend.models import Analysis

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    init_db()
