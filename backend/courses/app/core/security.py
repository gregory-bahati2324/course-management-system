# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import requests

from app.core.config import settings

# OAuth2 scheme for JWT Bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.AUTH_SERVICE_URL}/auth/login")

# JWT settings (must match the auth service)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def verify_token(token: str) -> dict:
    """Decode JWT token issued by auth service"""
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exc
        return payload
    except JWTError:
        raise credentials_exc


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Returns minimal user info needed by this service.
    Only contains: user_id and role.
    """
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")  # Include role in JWT payload
        if user_id is None or role is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    return {"user_id": user_id, "role": role}
