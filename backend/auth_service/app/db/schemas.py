from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


# Base user
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


# Signup user
class UserCreate(UserBase):
    password: str
    full_name: str
    student_id: Optional[str] = None
    year_of_study: Optional[str] = None


# Profiles
class AdminProfile(BaseModel):
    full_name: str
    permission: Optional[str] = None

    class Config:
        from_attributes = True


class InstructorProfile(BaseModel):
    full_name: str
    department: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True


class StudentProfile(BaseModel):
    full_name: str
    student_id: str
    year_of_study: str

    class Config:
        from_attributes = True

class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class InstructorCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    department: Optional[str] = None
    bio: Optional[str] = None

class StudentCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    student_id: str
    year_of_study: Optional[str] = "1"


class UserOut(BaseModel):
    id: UUID
    is_active: bool
    profile: Union[AdminProfile, InstructorProfile, StudentProfile]

    model_config = {"from_attributes": True}  # ensures Pydantic accepts SQLAlchemy ORM objects


# Update user
class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    student_id: Optional[str] = None  # required for student updates
    year_of_study: Optional[str] = None
    role: Optional[UserRole] = None  # normally should not change on update
    


# JWT tokens
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
