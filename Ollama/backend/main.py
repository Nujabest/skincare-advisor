from fastapi import FastAPI

# Import du router upload
from backend.routes import upload
from backend.routes import analyze 
from backend.routes import results

app = FastAPI()


@app.get("/")
def home():
    return {"message": "SkinCare Advisor API running"}



# On attache les routes à l'application
app.include_router(upload.router)
app.include_router(analyze.router) 
app.include_router(results.router)