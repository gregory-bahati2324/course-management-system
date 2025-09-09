from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List, Annotated
from uuid import UUID
from sqlalchemy.orm import Session

from app.db import schemas, crud
from app.db.database import get_db
from app.core.security import create_access_token, get_current_user
from app.core.config import settings

router = APIRouter()


@router.post("/signup/admin", response_model=schemas.UserOut)
def signup_admin(user_data: schemas.AdminCreate, db: Session = Depends(get_db)):
    """Create an admin user."""
    return crud.create_user(db, user_data, role=schemas.UserRole.ADMIN)


@router.post("/signup/instructor", response_model=schemas.UserOut)
def signup_instructor(user_data: schemas.InstructorCreate, db: Session = Depends(get_db)):
    """Create an instructor user."""
    return crud.create_user(db, user_data, role=schemas.UserRole.INSTRUCTOR)


@router.post("/signup/student", response_model=schemas.UserOut)
def signup_student(user_data: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Create a student user."""
    return crud.create_user(db, user_data, role=schemas.UserRole.STUDENT)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.email, "role": user.role, "user_id": str(user.id)}, expire_delta=access_token_expires)

    return {"access_token": token, "token_type": "bearer", "user_id": str(user.id), "role": user.role}


@router.get("/users/me", response_model=schemas.UserOut)
def get_me(current_user: schemas.UserOut = Depends(get_current_user)):
    """Get current logged-in user."""
    return current_user


@router.get("/users", response_model=List[schemas.UserOut])
def get_all_users(
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all users (admin only)."""
    if current_user["profile"].__class__.__name__.lower() != "adminprofile":
        raise HTTPException(status_code=403, detail="Only admin users can access this endpoint")
    return crud.get_all_users(db, skip=skip, limit=limit)


# -------------------
# Admin update
# -------------------
@router.put("/update/admin", response_model=schemas.UserOut)
def update_admin(
    data: schemas.AdminCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.profile.__class__ != schemas.AdminProfile:
        raise HTTPException(status_code=403, detail="Only admins can update this")
    return crud.update_user(db, current_user.id, data)


# -------------------
# Instructor update
# -------------------
@router.put("/update/instructor", response_model=schemas.UserOut)
def update_instructor(
    data: schemas.InstructorCreate,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.profile.__class__ != schemas.InstructorProfile:
        raise HTTPException(status_code=403, detail="Only instructors can update this")
    return crud.update_user(db, current_user.id, data)


# -------------------
# Student update
# -------------------
@router.put("/update/student", response_model=schemas.UserOut)
def update_student(
    data: schemas.UpdateUser,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.profile.__class__ != schemas.StudentProfile:
        raise HTTPException(status_code=403, detail="Only students can update this")
    return crud.update_user(db, current_user.id, data)


@router.delete("/delete/{user_id}", status_code=204)
def delete_user(
    user_id: UUID,
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only allow deletion if the user is deleting their own account
    # or if the current user is an admin
    if str(current_user.id) != str(user_id) and current_user.profile.__class__.__name__.lower() != "adminprofile":
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    crud.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}

