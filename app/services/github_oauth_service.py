from urllib.parse import urlencode
import httpx
from fastapi import HTTPException, status
from typing import Any
from app.core.config import settings

AUTH_URL  = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_URL  = "https://api.github.com/user"
EMAILS_URL= "https://api.github.com/user/emails"

def authorize_url(state: str) -> str:
    params: dict[str, str] = {
        "client_id": str(settings.GITHUB_CLIENT_ID),
        "redirect_uri": f"{settings.API_BASE_URL}/auth/github/callback",
        "scope": "read:user user:email",
        "state": state,
    }
    return f"{AUTH_URL}?{urlencode(params)}"

async def exchange_code_for_token(code: str) -> str:
    async with httpx.AsyncClient(timeout=15) as http_client:
        response = await http_client.post(
            TOKEN_URL,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": f"{settings.API_BASE_URL}/auth/github/callback",
            },
            headers={"Accept": "application/json"},
        )
        token_response = response.json()

    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="exchange_failed")
    return access_token

async def fetch_user_and_emails(access_token: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient(timeout=15) as http_client:
        user_response = await http_client.get(USER_URL, headers=headers)
        email_response = await http_client.get(EMAILS_URL, headers=headers)

    github_user = user_response.json()
    github_emails = email_response.json()
    return github_user, github_emails
