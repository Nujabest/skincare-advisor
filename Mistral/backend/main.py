from fastapi import FastAPI

from backend.routes.users import router as users_router
from backend.routes.analyze import router as ai_router
from backend.routes.analysis import router as analysis_router

app = FastAPI(
    title="SkinCare Advisor – Backend",
    version="1.0.0",
    description="API de base pour l'application SkinCare Advisor"
)

app.include_router(users_router)
app.include_router(ai_router)
app.include_router(analysis_router)

@app.get("/")
def home():
    return {"message": "SkinCare Advisor backend running!"}
