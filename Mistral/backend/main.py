from fastapi import FastAPI
from backend.routes.analyze import router as analyze_router
from backend.routes.test_mistral import router as test_router

app = FastAPI(title="SkinCare Advisor - Mistral")

app.include_router(analyze_router)
app.include_router(test_router)

@app.get("/")
def home():
    return {"message": "Mistral API running!"}
