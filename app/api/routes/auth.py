from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services import auth_service

router = APIRouter(tags=["Auth"])


@router.get("/login")
def login():
    """Redirect user to Google OAuth login page."""
    auth_url = auth_service.get_auth_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(code: str, state: str):
    """Google redirects here after user grants permission."""
    success = auth_service.exchange_code_for_token(code, state)

    if not success:
        return {"error": "State mismatch, possible CSRF attack"}

    return RedirectResponse("/liked-videos")


@router.get("/logout")
def logout():
    """Clear stored credentials."""
    auth_service.logout()
    return {"message": "Logged out successfully"}