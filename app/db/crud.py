from sqlalchemy.orm import Session
from app.db import models, schemas

# create a course
def create_course(db: Session, course: schemas.CourseCreate):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# Read all courses

def get_all_courses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Course).offset(skip).limit(limit).all()

# Read a course by ID
def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


# Update a course
def update_course(db: Session, course_id: int, course_data: schemas.CourseCreate):
    course = get_course_by_id(db, course_id)
    if course:
        for key, value in course_data.dict().items():
            setattr(course, key, value)
        db.commit()
        db.refresh(course)
    return course
    
# Delete a course
def delete_course(db: Session, course_id: int):
    course = get_course_by_id(db, course_id)
    if course:
        db.delete(course)
        db.commit()
    return course    
    
    
# create course structure item

def create_course_structure(db: Session, structure_data: schemas.CourseStructureCreate):
    structure = models.CourseStructure(**structure_data.dict())   
    db.add(structure)
    db.commit()
    db.refresh(structure)
    return structure

# GEt structure by course

def get_course_structure(db: Session, course_id: int):
    return db.query(models.CourseStructure).filter(models.CourseStructure.course_id==course_id).order_by(models.CourseStructure.order).all()
  
# Add a resource to a structure
def add_resource(db: Session, data: schemas.CourseResourceCreate):
    resource = models.CourseResourse(**data.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

# Get all resources for a structure
def get_resources(db: Session, structure_id: int):
    return db.query(models.CourseResourse).filter(models.CourseResource.structure_id == structure_id).all()
     