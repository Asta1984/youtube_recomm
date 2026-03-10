from google_auth_oauthlib.flow import Flow
from app.core.config import SCOPES, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from app.db import session_store


# Build config dict manually instead of loading from file
CLIENT_CONFIG = {
    "web": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI]
    }
}

def get_auth_url() -> str:
    flow = Flow.from_client_config(  
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        code_challenge_method="S256"
    )
    session_store.set("state", state)
    session_store.set("code_verifier", flow.code_verifier)
    return auth_url


def exchange_code_for_token(code: str, state: str) -> bool:
    if state != session_store.get("state"):
        return False

    flow = Flow.from_client_config(   
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    flow.fetch_token(code=code, code_verifier=session_store.get("code_verifier"))
    credentials = flow.credentials
    session_store.set("token", credentials.token)
    session_store.set("refresh_token", credentials.refresh_token)
    return True


def logout():
    """Clear all stored credentials."""
    session_store.clear()