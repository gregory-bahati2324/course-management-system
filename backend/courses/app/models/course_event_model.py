# models/progress_models.py
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.course_database import Base

class LessonProgress(Base):
    __tablename__ = "lesson_progress_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    student_id = Column(String, index=True, nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id"))
    is_completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    last_event = Column(String, nullable=True)  # e.g. "opened", "completed", "submitted"
    
    
    lesson = relationship("Lesson")
