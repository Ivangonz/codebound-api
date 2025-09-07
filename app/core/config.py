from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class Settings(BaseSettings):
    APP_NAME: str = "Codebound API"
    WEB_ORIGIN: HttpUrl = "http://localhost:5173"  # type: ignore
    API_BASE_URL: HttpUrl = "http://localhost:8000"  # type: ignore

    class Config:
        env_file = ".env"

settings = Settings()
