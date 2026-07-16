from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import categories, notes

app = FastAPI(title="DSA Pattern Notes API")

Base.metadata.create_all(bind=engine)

app.include_router(categories.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "DSA Pattern Notes API is running"}