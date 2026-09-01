from fastapi import FastAPI
import uvicorn
import os
from app.api.v1.clima import router as clima_router
from app.db.database import engine, Base
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Agregadora de Clima & Vestuário",
    description="API que sugere o que vestir com base na temperatura e condição do tempo.",
    version="1.0.0"
)

app.include_router(clima_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get("/", tags=["Healthcheck"])
def root():
    return {"status": "API online", "documentacao": "/docs"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)