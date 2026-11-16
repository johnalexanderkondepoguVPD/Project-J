from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Project-J: AI-powered Government Examination Intelligence Platform",
)

app.addMiddleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Project-J API", "version": settings.APP_VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}