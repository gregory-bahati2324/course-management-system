from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db import schemas, crud
from app.db.database import get_db
from app.core.config import settings
from app.models import user as models

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if password matches the hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Return hashed password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.UserOut:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    # Step 1: Get user by email
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise credentials_exc

    # Step 2: Get user with profile (SQLAlchemy object)
    profile_obj = None
    if user.role == schemas.UserRole.ADMIN:
        profile_obj = db.query(models.AdminProfile).filter(models.AdminProfile.id == user.id).first()
        profile_data = schemas.AdminProfile.from_orm(profile_obj)
    elif user.role == schemas.UserRole.INSTRUCTOR:
        profile_obj = db.query(models.InstructorProfile).filter(models.InstructorProfile.id == user.id).first()
        profile_data = schemas.InstructorProfile.from_orm(profile_obj)
    else:
        profile_obj = db.query(models.StudentProfile).filter(models.StudentProfile.id == user.id).first()
        profile_data = schemas.StudentProfile.from_orm(profile_obj)

    # Step 3: Return UserOut with correct Pydantic profile
    return schemas.UserOut(id=user.id, is_active=user.is_active, profile=profile_data)
