from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.core.database import init_db
from src.api import enroll, verify, identify, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Face Recognition Cloud System",
    description="Master 2 RISR - Université de Saida Dr. Moulay Tahar",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(enroll.router, prefix="/api/v1")
app.include_router(verify.router, prefix="/api/v1")
app.include_router(identify.router, prefix="/api/v1")

# Static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "Face Recognition Cloud System",
        "university": "Université de Saida - Dr. Moulay Tahar",
        "program": "Master 2 RISR",
        "version": "1.0.0",
        "docs": "/docs",
        "ui": "/static/index.html"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "system": "operational"}
