from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from app.db.course_database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


# ------------------ Course ------------------
class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    instructor_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    category = Column(String(50), nullable=True)

# ------------------ Enrollment ------------------
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    student_id = Column(String, index=True, nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

# ------------------ Module ------------------
class Module(Base):
    __tablename__ = "modules"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    title = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

# ------------------ Lesson ------------------
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=True)
    duration_days = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False)
    video_url = Column(String(255), nullable=True)
    document_url = Column(String(255), nullable=True)
    
    materials = relationship("LessonMaterial", back_populates="lesson", cascade="all, delete-orphan")
    
class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    student_id = Column(String, index=True, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)  
    progress_percentage = Column(Integer, default=0, nullable=False)  
