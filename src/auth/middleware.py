from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request
from settings import OIDC_ENABLED

PUBLIC_PATHS = ["/login", "/auth/callback", "/logout", "/static", "/favicon.ico"]

class AuthRequiredMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if not OIDC_ENABLED or scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        path = request.url.path
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            await self.app(scope, receive, send)
            return

        if not request.session.get("user"):
            response = RedirectResponse("/login")
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
