# schemas/progress_schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LessonProgressEvent(BaseModel):
    student_id: str
    lesson_id: str
    event: str   # e.g. "opened", "completed", "submitted"

class LessonProgressOut(BaseModel):
    id: str
    student_id: str
    lesson_id: str
    is_completed: bool
    last_accessed: datetime
    last_event: Optional[str]

    class Config:
        orm_mode = True
