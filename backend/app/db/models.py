from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.db.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    objectives = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    visibility = Column(String, default="private")
    instructor = Column(String, nullable=False)
    is_published = Column(Boolean, default=False)
    
    
    
class CourseStructure(Base):
    __tablename__="course_structure"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    order = Column(Integer, default=1)    
    
class CourseResourse(Base):
    __tablename__ = "course_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    structure_id = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # pdf, video, link
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    
    
# pre-requisites for courses
class Prerequisite(Base):
    __tablename__ = "prerequisites"
    
    id = Column(Integer, primary_key=True, index=True)
    structure_id = Column(Integer, ForeignKey("course_structure.id"), nullable=False)
    prerequisite_id = Column(Integer, ForeignKey("course_structure.id"), nullable=False)
    
# track progress
class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    structure_id = Column(Integer, ForeignKey("course_structure.id"), nullable=False)
    student = Column(String, nullable=False)
    