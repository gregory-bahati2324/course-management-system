from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from uuid import uuid4
import os


from app.core.security import get_current_user
from app.db import user_service_crud, user_profile_schemas
from app.db.user_database import get_db
import uuid

router = APIRouter()
UPLOAD_DIR = "app/static/profile_pics"

@router.put("/profile", response_model=user_profile_schemas.UserProfileOut)
def create_profile(
    profile_data: user_profile_schemas.UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    # verify user is authenticated
    if str(profile_data.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create a profile for yourself."
        )
        
        
    try:
        return user_service_crud.create_user_profile(db, profile_data)
    except HTTPException as e:
        raise e    

@router.get("/profile", response_model=user_profile_schemas.UserProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get the profile of the current user."""
    user_id = str(current_user.id)
    profile = user_service_crud.get_profile_by_user_id(db, user_id=user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found."
        )
    return user_profile_schemas.UserProfileOut.from_orm(profile)


@router.patch("/profile", response_model=user_profile_schemas.UserProfileOut)
def update_my_profile(
    profile_data: user_profile_schemas.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user.id)
    updated_profile = user_service_crud.update_user_profile(db, user_id=user_id, profile_data=profile_data)
    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found."
        )
        
    return updated_profile    


@router.post("/profile/picture", response_model=user_profile_schemas.UserProfileOut)
def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image."
        )
        
    # generate unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    
    # save the file
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
    # update user profile with picture path
    profile = user_service_crud.get_profile_by_user_id(db, str(current_user.id))
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found."
        )
    profile.profile_picture_path = file_path
    db.commit()
    db.refresh(profile) 
    
    return user_profile_schemas.UserProfileOut.from_orm(profile)         
    

@router.get("/profile/picture")
def get_profile_picture(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    profile = user_service_crud.get_profile_by_user_id(db, str(current_user.id))
    if not profile or not profile.profile_picture_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile picture not found."
        )
    # return the file response
    return FileResponse(profile.profile_picture_path)    