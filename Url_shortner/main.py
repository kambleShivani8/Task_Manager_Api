from fastapi import FastAPI
from database import engine, Base
from routers.shortener import router as shortener_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")
app.include_router(shortener_router)

