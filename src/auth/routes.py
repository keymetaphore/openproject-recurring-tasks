from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from settings import OIDC_ENABLED, OIDC_REDIRECT_URI
from auth.oidc import oauth

router = APIRouter()

if OIDC_ENABLED:
    @router.get("/login")
    async def login(request: Request):
        return await oauth.oidc.authorize_redirect(request, OIDC_REDIRECT_URI)

    @router.get("/auth/callback")
    async def auth_callback(request: Request):
        token = await oauth.oidc.authorize_access_token(request)
        user = await oauth.oidc.userinfo(token=token)
        request.session["user"] = dict(user)
        return RedirectResponse(url="/")

    @router.get("/logout")
    async def logout(request: Request):
        request.session.clear()
        return RedirectResponse(url="/")
