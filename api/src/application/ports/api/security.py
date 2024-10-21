from typing import Coroutine, Any, Callable

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware


def get_api_token_validator(api_token: str) -> Callable[..., Coroutine[Any, Any, str]]:
    async def check_auth_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if credentials.credentials != api_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API Key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials.credentials

    return check_auth_token


def setup_allowed_hosts(app: FastAPI, hosts: list[str]) -> None:
    if hosts:
        app.add_middleware(
            TrustedHostMiddleware, allowed_hosts=hosts
        )


def setup_cors(app: FastAPI, origins: list[str]) -> None:
    if origins:
        app.add_middleware(
            CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
        )
