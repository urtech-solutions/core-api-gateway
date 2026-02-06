from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.auth import create_access_token
from app.config import settings
from app.middleware import JWTAuthMiddleware
from app.proxy import forward_request

app = FastAPI(title="core-api-gateway", version="0.1.0")
app.add_middleware(JWTAuthMiddleware)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/login")
async def login(payload: LoginRequest) -> dict[str, str]:
    _ = payload.password
    token = create_access_token(payload.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me")
async def me(request: Request) -> dict[str, str | None]:
    return {"username": getattr(request.state, "user", None)}


@app.api_route("/devices{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_devices(request: Request, path: str = ""):
    return await forward_request(request, settings.device_registry_url, f"/devices{path}")


@app.api_route("/status{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_status(request: Request, path: str = ""):
    return await forward_request(request, settings.telemetry_api_url, f"/status{path}")


@app.api_route("/telemetry{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_telemetry(request: Request, path: str = ""):
    return await forward_request(request, settings.telemetry_api_url, f"/telemetry{path}")
