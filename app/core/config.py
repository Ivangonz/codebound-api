from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class Settings(BaseSettings):
    APP_NAME: str = "Codebound API"
    WEB_ORIGIN: HttpUrl = "http://localhost:5173"  # type: ignore
    API_BASE_URL: HttpUrl = "http://localhost:8000"  # type: ignore
    GITHUB_CLIENT_ID: str = "your_github_client_id_here"
    GITHUB_CLIENT_SECRET: str = "your_github_client_secret_here"

    class Config:
        env_file = ".env"

settings = Settings()
