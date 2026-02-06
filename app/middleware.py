from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.auth import decode_token

EXCLUDED_PATHS = {"/healthz", "/auth/login", "/docs", "/openapi.json", "/redoc"}


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        auth = request.headers.get("authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing bearer token"})

        token = auth.removeprefix("Bearer ").strip()
        try:
            payload = decode_token(token)
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        request.state.user = payload.get("sub")
        return await call_next(request)
