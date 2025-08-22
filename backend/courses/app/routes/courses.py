from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from typing import List
from typing import List, Optional
from app.db.course_database import get_db
from app.db import course_crud, event_based_crud, lesson_material_crud
from app.db import course_schemas, course_event_schemas, lesson_material_schemas
from app.models import course_models, course_event_model
from app.db.lesson_material_crud import save_lesson_material, get_lesson_materials, get_lesson_material_by_id
from app.db.lesson_material_schemas import LessonMaterialResponse
from app.core.security import get_current_user

router = APIRouter()

@router.post("/courses/", response_model=course_schemas.CourseOut)
def create_course(
    course: course_schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify current user is an instructor
    if current_user["role"] != "instructor":
        raise HTTPException(status_code=403, detail="Only instructors can create courses")

    return course_crud.create_course(db=db, course=course)


@router.post("/enrollments/", response_model=course_schemas.EnrollmentOut)
def enroll_in_course(
    enrollment: course_schemas.EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify current user is a student
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can enroll in courses")

    return course_crud.create_enrollment(db=db, enrollment=enrollment)

@router.post("/courses/{course_id}/modules/", response_model=course_schemas.ModuleOut)
def create_module(
    course_id: uuid.UUID,
    module: course_schemas.ModuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    course_id = str(course_id)
    module.course_id = str(module.course_id)
    # verify course exist and user is instructor
    db_course = course_crud.get_course(db, course_id)
    if not db_course or current_user["role"] != "instructor":
        raise HTTPException(status_code=404, detail="Course not found or not authorized")

    return course_crud.create_module(db, module)

@router.post("/modules/{module_id}/lessons", response_model=course_schemas.LessonOut)
def create_module_lesson(
    module_id: str,
    lesson: course_schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify module exist
    db_module = db.query(course_models.Module).filter(
        course_models.Module.id == module_id
    ).first()
    
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # check authorization
    db_course = course_crud.get_course(db, db_module.course_id)
    if current_user["role"] != "instructor":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # ✅ pass module_id explicitly
    return course_crud.create_lesson(db, lesson, module_id)


@router.get("/courses/search", response_model=List[course_schemas.CourseOut])
def Search_courses(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    instructor_id: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    filters = course_schemas.CourseFilter(
        search=search,
        category=category,
        instructor_id=instructor_id,
        is_published=is_published
    )
    return course_crud.search_courses(db, filters)

@router.post("/lessons/{lesson_id}/complete", response_model=course_schemas.LessonProgressOut)
def complete_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify current user is a student
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can complete lessons")

    # check if lesson exists
    db_lesson = db.query(course_models.Lesson).filter(
        course_models.Lesson.id == lesson_id
    ).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    progress_in_db = course_crud.get_lesson_progress(db, lesson_id, current_user["user_id"])
    if progress_in_db:
        raise HTTPException(status_code=400, detail="Lesson already completed")

    # mark lesson as complete
    progress = course_schemas.LessonProgressCreate(
        lesson_id=lesson_id,
        student_id=current_user["user_id"],
        progress_percentage=100
    )
    return course_crud.mark_lesson_complete(db, progress)


# Get progress for a single course
@router.get("/lessons/{lesson_id}/progress/{student_id}")
def get_lesson_progress(
    lesson_id: str,
    student_id: str,
    db: Session = Depends(get_db)
):
    progress = course_crud.get_lesson_progress(db, lesson_id, student_id)
    if not progress:
        return {"lesson_id": lesson_id, "student_id": student_id, "progress_percentage": 0, "completed": False}
    
    return {
        "lesson_id": lesson_id,
        "student_id": student_id,
        "progress_percentage": progress.progress_percentage,
        "completed": progress.progress_percentage == 100
    }
    
    
# get course details
@router.get("/lessons/{lesson_id}", response_model=lesson_material_schemas.LessonDetail)
def get_lesson_details(
    lesson_id: str,
    db: Session = Depends(get_db)
):
    lesson = lesson_material_crud.get_lesson_details(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return lesson

# 

# Get progress for a course
@router.get("/courses/{course_id}/progress/{student_id}")
def get_course_progress(
    course_id: str,
    student_id: str,
    db: Session = Depends(get_db)
):
    progress = course_crud.get_course_progress(db, course_id, student_id)
    if not progress:
        return {"course_id": course_id, "student_id": student_id, "total_lessons": 0, "completed_lessons": 0, "is_course_completed": False, "progress_percentage": 0}
    
    return {
        "course_id": course_id,
        "student_id": student_id,
        "total_lessons": progress["total_lessons"],
        "completed_lessons": progress["completed_lessons"],
        "is_course_completed": progress["is_course_completed"],
        "progress_percentage": progress["progress_percentage"]
    }   
    
@router.post("/lessons/progress/event", response_model=course_event_schemas.LessonProgressOut)  
def track_event(
    event: course_event_schemas.LessonProgressEvent,
    db: Session = Depends(get_db)
):
    """Record a lesson progress event (e.g., opened, completed)"""
    return event_based_crud.record_event(db, event)

@router.get("/lessons/{lesson_id}/progress/{student_id}", response_model=course_event_schemas.LessonProgressOut)
def get_lesson_progress_event(lesson_id: str, student_id: str, db: Session = Depends(get_db)):
    """Get the progress of a specific lesson for a student"""
    return db.query(course_event_model.LessonProgress).filter_by(
        lesson_id=lesson_id,
        student_id=student_id
    ).first() 
    
    
# Upload lesson materials
@router.post("/lessons/{lesson_id}/materials/", response_model=List[LessonMaterialResponse])
def upload_lesson_materials(
    lesson_id: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    lesson = db.query(course_models.Lesson).filter(
        course_models.Lesson.id == lesson_id
    ).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return save_lesson_material(db, lesson_id, files)

# Download lesson material
@router.get("/lessons/{lesson_id}/materials", response_model=List[LessonMaterialResponse])
def list_lesson_materials(
    lesson_id: str,
    db: Session = Depends(get_db)
):
    materials = get_lesson_materials(db, lesson_id)
    if not materials:
        raise HTTPException(status_code=404, detail="No materials found for this lesson")
    return materials

# Download specific lesson material by ID
@router.get("/materials/{material_id}/download")
def download_lesson_material(
    material_id: str,
    db: Session = Depends(get_db)
):
    material = get_lesson_material_by_id(db, material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    file_url = Path(material.file_url)
    if not file_url.exists() or not file_url.is_file():
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(path=file_url, filename=file_url.name, media_type='application/octet-stream')