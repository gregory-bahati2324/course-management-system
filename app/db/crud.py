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
    return db.query(models.CourseResourse).filter(models.CourseResourse.structure_id == structure_id).all()
     
     
# Edit a structure item
def updata_structure(db: Session, structure_id: int, update_data: schemas.CourseStructureCreate):
    structure = db.query(models.CourseStructure).filter(models.CourseStructure.id == structure_id).first()
    if structure:
        for key, value in update_data.dict().items():
            setattr(structure, key, value)
        db.commit()
        db.refresh(structure)
    return structure

# Delete a structure item
def delete_structure(db: Session, structure_id: int):
    structure = db.query(models.CourseStructure).filter(models.CourseStructure.id == structure_id).first()
    if structure:
        db.delete(structure)
        db.commit()
    return structure

# Create a prerequisite
def add_prerequisite(db: Session, data: schemas.PrerequisiteCreate):
    item = models.Prerequisite(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item        

def get_prerequisites(db: Session, structure_id: int):
    return db.query(models.Prerequisite).filter(models.Prerequisite.structure_id == structure_id).all()
     
     
def update_progress(db: Session, data: schemas.ProgressUpdata):
    record = db.query(models.Progress).filter(
        models.Progress.student_id == data.student_id,
        models.Progress.structure_id == data.structure_id
    ).first()
    
    if record:
        record.is_completed = data.is_completed
    else:
        record = models.Progress(**data.dict())
        db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_progress(db: Session, student_id: int):
    return db.query(models.Progress).filter(models.Progress.student_id == student_id).all()   
                 