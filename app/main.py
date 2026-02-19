from fastapi import FastAPI

from app.database import Base, engine
from app.routers import routers
from app.auth.auth_routes import router as auth_router




app = FastAPI(title="Task Manager API")

app.include_router(routers.router)

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
