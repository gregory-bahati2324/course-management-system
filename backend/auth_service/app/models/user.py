from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
import uuid
from enum import Enum as PyEnum
from app.db.database import Base

class UserRole(str, PyEnum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)

class AdminProfile(Base):
    __tablename__ = "admin_profiles"
    id = Column(String, ForeignKey("users.id"), primary_key=True)
    full_name = Column(String, nullable=False)
    permission = Column(String)

class InstructorProfile(Base):
    __tablename__ = "instructor_profiles"
    id = Column(String, ForeignKey("users.id"), primary_key=True)
    full_name = Column(String, nullable=False)
    department = Column(String)
    bio = Column(String)

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    id = Column(String, ForeignKey("users.id"), primary_key=True)
    full_name = Column(String, nullable=False)
    student_id = Column(String, unique=True, nullable=False)
    year_of_study = Column(String)
