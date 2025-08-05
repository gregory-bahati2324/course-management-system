from pydantic import BaseModel
from datetime import date

class CourseCreate(BaseModel):
    title: str
    description: str
    objectives: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    visibility: str = "private"
    instructor: str
    is_published: bool = False
    
    
class CourseStructureCreate(BaseModel):
    course_id: int
    type: str
    title: str
    content: str | None = None
    order: int = 1    
    
class CourseOut(BaseModel):
    id: int
    
    class Config:
        orm_mode = True
        
        
class CourseStructureOut(CourseStructureCreate):
    id: int
    
    class Config:
        orm_mode = True        
        
        
class CoursePreview(BaseModel):
    title: str
    description: str
    instructor: str
    
    class Config:
        orm_mode = True        
        
class CourseResourceCreate(BaseModel):
    structure_id: int
    type: str
    title: str
    url: str | None = None
    notes: str | None = None

class CourseResourceOut(CourseResourceCreate):
    id: int

    class Config:
        orm_mode = True
        
        
class PrerequisiteCreate(BaseModel):
    structure_id: int
    prerequisite_id: int
    
class PrerequisiteOut(PrerequisiteCreate):
    id: int
    structure_id: int
    prerequisite_id: int

    class Config:
        orm_mode = True
        
class ProgressCreate(BaseModel):
    student: str
    structure_id: int

class ProgressOut(BaseModel):
    id: int
    student: str
    structure_id: int

    class Config:
        orm_mode = True  
        