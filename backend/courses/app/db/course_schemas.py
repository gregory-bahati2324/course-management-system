from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_published: bool = False
    
class CourseCreate(CourseBase):
    instructor_id: str
    
class CourseOut(CourseBase):
    id: uuid.UUID
    instructor_id: str
    is_published: bool = False
    created_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
        
        
class EnrollmentCreate(BaseModel):
    course_id: uuid.UUID
    student_id: str
    
class EnrollmentOut(EnrollmentCreate):
    id: uuid.UUID
    enrolled_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True        
        
class ModuleBase(BaseModel):
    title: str = Field(..., max_length=100)
    position: int
    description: Optional[str] = None
    
class ModuleCreate(ModuleBase):
    course_id: uuid.UUID  
    
class ModuleOut(ModuleBase):
    id: uuid.UUID
    course_id: uuid.UUID
    created_at: datetime = datetime.utcnow()
    
    class Config:
        from_attributes = True
        
class LessonBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: Optional[str] = None
    duration_days: Optional[int] = None
    position: int
    video_url: Optional[str] = None
    document_url: Optional[str] = None
    
    
class LessonCreate(LessonBase):
    module_id: str
    
class LessonOut(LessonBase):
    id: uuid.UUID
    module_id: uuid.UUID
    created_at: datetime = datetime.utcnow()
    
    class Config:
        from_attributes = True
        
        
# search and filter schemas
class CourseFilter(BaseModel):
    search: Optional[str] = None
    category: Optional[str] = None
    instructor_id: Optional[str] = None
    is_published: Optional[bool] = None
    duration_days: Optional[int] = Field(None, ge=0, description="Minimum duration in days for filtering courses")
                                           