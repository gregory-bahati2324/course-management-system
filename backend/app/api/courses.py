from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
import shutil
import os
from sqlalchemy.orm import Session
from typing import List
from app.db import models, schemas
from fastapi import Depends




from app.db import crud, schemas
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# Create a course
@router.post("/", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course)


# Read all courses
@router.get("/", response_model=List[schemas.CourseOut])
def get_courses(db: Session = Depends(get_db)):
    return crud.get_all_courses(db)

@router.get("/{course_id}", response_model=schemas.CoursePreview)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course



# Update a course
@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, updated_data: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = crud.update_course(db, course_id, updated_data)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

# Delete a course
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return {"detail": "Course deleted successfully"}


@router.post("/structure/", response_model=schemas.CourseStructureOut)
def create_structure(structure: schemas.CourseStructureCreate, db: Session = Depends(get_db)):
    return crud.create_course_structure(db, structure)

@router.get("/{course_id}/structure", response_model=List[schemas.CourseStructureOut])
def get_structure(course_id: int, db: Session = Depends(get_db)):
    return crud.get_course_structure(db, course_id)

@router.post("/structure/resources/", response_model=schemas.CourseResourceOut)
def create_resource(resource: schemas.CourseResourceCreate, db: Session = Depends(get_db)):
    return crud.add_resource(db, resource)

@router.get("/structure/{structure_id}/resources/", response_model=List[schemas.CourseResourceOut])
def list_resources(structure_id: int, db: Session = Depends(get_db)):
    return crud.get_resources(db, structure_id)


UPLOAD_DIR = "uploads/"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/structure/upload/", response_model=schemas.CourseResourceOut)
def upload_file_resource(
    structure_id: int = Form(...),
    title: str = Form(...),
    type: str = Form(...),
    notes: str = Form(""),
    url: str = Form(""),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    filename = f"{UPLOAD_DIR}{file.filename}"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    data = schemas.CourseResourceCreate(
        structure_id=structure_id,
        type=type,
        title=title,
        url=filename,
        notes=notes
    )    
    return crud.add_resource(db, data)


@router.put("/structure/{structure_id}", response_model=schemas.CourseStructureOut)
def edit_structure(
    structure_id: int,
    updated_data: schemas.CourseStructureCreate,
    db: Session = Depends(get_db)
):
    return crud.updata_structure(db, structure_id, updated_data)

@router.delete("/structure/{structure_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_structure(structure_id: int, db: Session = Depends(get_db)):
    return crud.delete_structure(db, structure_id)

@router.post("/structure/prerequisite/", response_model=schemas.PrerequisiteOut)
def create_prerequisite(
    structure_id: int = Form(...),
    prerequisite_id: int = Form(...),
    db: Session = Depends(get_db)
):
    print("Received structure_id:", structure_id)
    print("Received prerequisite_id:", prerequisite_id)

    data = schemas.PrerequisiteCreate(
        structure_id=structure_id,
        prerequisite_id=prerequisite_id
    )
    return crud.add_prerequisite(db, data)

@router.get("/structure/{structure_id}/prerequisites", response_model=List[schemas.PrerequisiteOut])
def get_prerequisites(structure_id: int, db: Session = Depends(get_db)):
    return db.query(models.Prerequisite).filter(models.Prerequisite.structure_id == structure_id).all()

@router.post("/structure/progress/", response_model=schemas.ProgressOut)
def track_progress(
    student: str = Form(...),
    structure_id: int = Form(...),
    db: Session = Depends(get_db)
):
    data = schemas.ProgressCreate(student=student, structure_id=structure_id)
    return crud.track_progress(db, data)

@router.get("/structure/progress/{student}", response_model=List[schemas.ProgressOut])
def get_user_progress(student: str, db: Session = Depends(get_db)):
    return crud.get_progress_for_user(db, student)
