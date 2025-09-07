from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

def add_cors(app: FastAPI) -> None:
    allowed = {str(settings.WEB_ORIGIN)}
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(allowed),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
