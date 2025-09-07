import secrets
import json
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from app.core.config import settings
from app.services import github_oauth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/github/url")
def github_url():
    # Generate state token for CSRF protection
    state_token = secrets.token_hex(24)
    url = github_oauth_service.authorize_url(state_token)
    return {"authorize_url": url, "state": state_token}

@router.get("/github/callback")
async def github_callback(request: Request):
    code = request.query_params.get("code")
    state_token = request.query_params.get("state")

    if not code or not state_token:
        return JSONResponse({"error": "missing_code_or_state"}, status_code=status.HTTP_400_BAD_REQUEST)

    access_token = await github_oauth_service.exchange_code_for_token(code)
    github_user, github_emails = await github_oauth_service.fetch_user_and_emails(access_token)

    # 🔎 For now, just log the response
    print("[OAuth] GitHub user:", json.dumps(github_user, indent=2)[:800])
    print("[OAuth] Emails:", json.dumps(github_emails, indent=2)[:800])

    return RedirectResponse(f"{settings.WEB_ORIGIN}/login/success?debug=1", status_code=302)
