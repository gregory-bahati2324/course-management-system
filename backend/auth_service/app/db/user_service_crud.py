from sqlalchemy.orm import Session
from app.models import profile as models
from app.db import user_profile_schemas
from fastapi import HTTPException, status
import uuid

def get_profile_by_user_id(db: Session, user_id):
    """Get user profile by user ID."""
    user_id = str(user_id)
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def create_user_profile(db: Session, profile_data: user_profile_schemas.UserProfileCreate):
    # check if profile already exists
    existing_profile = get_profile_by_user_id(db, profile_data.user_id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user."
        )
        
    db_profile = models.UserProfile(
        user_id=str(profile_data.user_id),
        full_name=profile_data.full_name,
        bio=profile_data.bio,
        website=str(profile_data.website) if profile_data.website else None,
        location=profile_data.location,
        phone_number=profile_data.phone_number
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return user_profile_schemas.UserProfileOut.from_orm(db_profile)

def update_user_profile(db: Session, user_id: str, 
                        profile_data: user_profile_schemas.UserProfileUpdate):
    user_id = str(user_id)
    db_profile = get_profile_by_user_id(db, user_id)
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found."
        )
        
    update_data = profile_data.model_dump(exclude_unset=True)

    if "website" in update_data and update_data["website"] is not None:
        update_data["website"] = str(update_data["website"])

    for field, value in update_data.items():
        setattr(db_profile, field, value)
        
    db.commit()
    db.refresh(db_profile)
    return user_profile_schemas.UserProfileOut.from_orm(db_profile)      


      