from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
from app.models import Base
from app.routers import auth, categories, notes

app = FastAPI(title="DSA Pattern Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:4321",
        "http://localhost:4321",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "DSA Pattern Notes API is running"}
