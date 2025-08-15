from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status
from app.db import schemas
from app.models import user as models
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    """Return a user object by email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, sign_user, role: schemas.UserRole):
    """
    Create a user and their profile safely.
    No partial creation — if any validation fails, nothing is saved.
    """

    # 1️⃣ Check if email is already taken
    if get_user_by_email(db, sign_user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2️⃣ Additional validation per role
    if role == schemas.UserRole.STUDENT:
        if not sign_user.student_id:
            raise HTTPException(status_code=400, detail="Student ID is required")
        existing_student = db.query(models.StudentProfile).filter(
            models.StudentProfile.student_id == sign_user.student_id
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="Student ID already exists")

    # You can add extra validations for admin/instructor if needed
    # For example, instructor might require department
    if role == schemas.UserRole.INSTRUCTOR:
        if not getattr(sign_user, "full_name", None):
            raise HTTPException(status_code=400, detail="Instructor full name is required")

    if role == schemas.UserRole.ADMIN:
        if not getattr(sign_user, "full_name", None):
            raise HTTPException(status_code=400, detail="Admin full name is required")

    try:
        # 3️⃣ Create the main user object
        db_user = models.User(
            email=sign_user.email,
            password_hash=get_password_hash(sign_user.password),
            role=role
        )
        db.add(db_user)
        db.flush()  # assign ID without committing

        # 4️⃣ Create role-specific profile
        if role == schemas.UserRole.ADMIN:
            profile = models.AdminProfile(id=db_user.id, full_name=sign_user.full_name)
        elif role == schemas.UserRole.INSTRUCTOR:
            profile = models.InstructorProfile(id=db_user.id, full_name=sign_user.full_name)
        else:  # STUDENT
            profile = models.StudentProfile(
                id=db_user.id,
                full_name=sign_user.full_name,
                student_id=sign_user.student_id,
                year_of_study=sign_user.year_of_study or "1"
            )

        db.add(profile)

        # 5️⃣ Commit everything at once
        db.commit()
        db.refresh(db_user)
        db.refresh(profile)

    except Exception as e:
        db.rollback()  # rollback if anything goes wrong
        raise HTTPException(status_code=500, detail=str(e))

    # 6️⃣ Return user with profile
    return get_user_with_profile(db, db_user.id)




def authenticate_user(db: Session, email: str, password: str):
    """Return user if password matches."""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_profile_by_user(db: Session, user: models.User):
    """Helper to get profile based on role."""
    if user.role == schemas.UserRole.ADMIN:
        return db.query(models.AdminProfile).filter(models.AdminProfile.id == user.id).first()
    elif user.role == schemas.UserRole.INSTRUCTOR:
        return db.query(models.InstructorProfile).filter(models.InstructorProfile.id == user.id).first()
    else:
        return db.query(models.StudentProfile).filter(models.StudentProfile.id == user.id).first()

def get_user_with_profile(db: Session, user_id: UUID):
    """Get a user and profile together."""
    user = db.query(models.User).filter(models.User.id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = get_profile_by_user(db, user)
    return {
        "id": user.id,
        "is_active": user.is_active,
        "profile": profile
    }

def update_user(db: Session, user_id: UUID, data: schemas.UpdateUser):
    """Update any user safely, handling duplicates and profile fields."""
    db_user = db.query(models.User).filter(models.User.id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = data.model_dump(exclude_unset=True)

    # -------------------
    # Check for duplicate email
    # -------------------
    if "email" in update_dict:
        existing_user = db.query(models.User).filter(models.User.email == update_dict["email"]).first()
        if existing_user and existing_user.id != str(user_id):
            raise HTTPException(status_code=400, detail="Email already exists")

    # -------------------
    # Check for duplicate student_id
    # -------------------
    if db_user.role == schemas.UserRole.STUDENT and "student_id" in update_dict:
        existing_student = db.query(models.StudentProfile).filter(
            models.StudentProfile.student_id == update_dict["student_id"]
        ).first()
        if existing_student and existing_student.id != str(user_id):
            raise HTTPException(status_code=400, detail="Student ID already exists")

    # -------------------
    # Handle password update
    # -------------------
    if "password" in update_dict:
        update_dict["password_hash"] = get_password_hash(update_dict.pop("password"))

    # -------------------
    # Update user attributes
    # -------------------
    for key, value in update_dict.items():
        if key not in ["full_name", "student_id", "year_of_study"]:  # These go to profile
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    # -------------------
    # Update profile fields
    # -------------------
    profile_obj = None
    profile_data = None

    if db_user.role == schemas.UserRole.ADMIN:
        profile_obj = db.query(models.AdminProfile).filter(models.AdminProfile.id == db_user.id).first()
        if "full_name" in update_dict:
            profile_obj.full_name = update_dict["full_name"]
        db.commit()
        db.refresh(profile_obj)
        profile_data = schemas.AdminProfile.from_orm(profile_obj)

    elif db_user.role == schemas.UserRole.INSTRUCTOR:
        profile_obj = db.query(models.InstructorProfile).filter(models.InstructorProfile.id == db_user.id).first()
        if "full_name" in update_dict:
            profile_obj.full_name = update_dict["full_name"]
        db.commit()
        db.refresh(profile_obj)
        profile_data = schemas.InstructorProfile.from_orm(profile_obj)

    else:  # Student
        profile_obj = db.query(models.StudentProfile).filter(models.StudentProfile.id == db_user.id).first()
        if "full_name" in update_dict:
            profile_obj.full_name = update_dict["full_name"]
        if "student_id" in update_dict:
            profile_obj.student_id = update_dict["student_id"]
        if "year_of_study" in update_dict:
            profile_obj.year_of_study = update_dict["year_of_study"]
        db.commit()
        db.refresh(profile_obj)
        profile_data = schemas.StudentProfile.from_orm(profile_obj)

    return schemas.UserOut(id=db_user.id, is_active=db_user.is_active, profile=profile_data)


def delete_user(db: Session, user_id: UUID):
    """Delete a user and their profile safely."""
    db_user = db.query(models.User).filter(models.User.id == str(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # -------------------
    # Delete profile first based on role
    # -------------------
    if db_user.role == schemas.UserRole.ADMIN:
        db.query(models.AdminProfile).filter(models.AdminProfile.id == db_user.id).delete()

    elif db_user.role == schemas.UserRole.INSTRUCTOR:
        db.query(models.InstructorProfile).filter(models.InstructorProfile.id == db_user.id).delete()

    elif db_user.role == schemas.UserRole.STUDENT:
        db.query(models.StudentProfile).filter(models.StudentProfile.id == db_user.id).delete()

    # -------------------
    # Delete the main user record
    # -------------------
    db.delete(db_user)
    db.commit()

    return {"detail": "User and profile deleted successfully"}



def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with profiles."""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return [get_user_with_profile(db, user.id) for user in users]
