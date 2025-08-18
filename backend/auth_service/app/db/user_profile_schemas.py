from pydantic import BaseModel, HttpUrl
from typing import Optional
from uuid import UUID

class UserProfileBase(BaseModel):
    full_name: str
    bio: Optional[str] = None
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    
class UserProfileCreate(UserProfileBase):
    user_id: UUID
    
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    
class UserProfileOut(UserProfileBase):
    id: int
    user_id: UUID
    is_verified: bool = False
    profile_picture_path: Optional[str] = None
    
    class Config:
        from_attributes = True      
    
    