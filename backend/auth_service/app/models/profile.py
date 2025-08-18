from xxlimited import Str
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db.user_database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    # primary key for user profile
    id = Column(Integer, primary_key=True, index=True)
    # foreign key to user table
    user_id = Column(String,index=True, unique=True, nullable=False)
    # profile specific fields
    full_name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    profile_picture_path = Column(String, nullable=True)
    
    # verification fields
    is_verified = Column(Boolean, default=False)
    
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    