from fastapi import Request
from fastapi.responses import RedirectResponse
from settings import OIDC_ENABLED

def require_user(request: Request):
    if not OIDC_ENABLED:
        return None
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login")
    return user