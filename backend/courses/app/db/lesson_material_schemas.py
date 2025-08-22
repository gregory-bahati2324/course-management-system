from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class LessonMaterialBase(BaseModel):
    file_url: str
    
class LessonMaterialCreate(LessonMaterialBase):
    lesson_id: str
    
class LessonMaterialResponse(LessonMaterialBase):
    id: str
    filename: str
    uploaded_at: datetime

    class Config:
        orm_mode = True
        
class LessonDetail(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    module_id: str
    materials: List[LessonMaterialResponse] = []

    class Config:
        orm_mode = True