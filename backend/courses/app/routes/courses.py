from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
import uuid
from typing import List, Optional
from app.db.course_database import get_db
from app.db import course_crud
from app.db import course_schemas
from app.models import course_models
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
    if str(enrollment.student_id) != str(current_user.get("user_id")):
        raise HTTPException(status_code=403, detail="You are not authorized to enroll in this course.")
    
    return course_crud.create_enrollment(db=db, enrollment=enrollment)

@router.post("/courses/{course_id}/modules/", response_model=course_schemas.ModuleOut)
def create_module(
    course_id: uuid.UUID,
    module: course_schemas.ModuleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify course exist and user is instructor
    db_course = course_crud.get_course(db, course_id)
    if not db_course or str(db_course.instructor_id) != current_user["user_id"]:
        raise HTTPException(status_code=4004, detail="Course not found or not authorized")

    return course_crud.create_module(db, module)
@router.post("/modules/{module_id}/lessons", response_model=course_schemas.LessonOut)
def create_module_lesson(
    module_id: uuid.UUID,
    lesson: course_schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # verify module exist and user is instructor
    db_module = db.query(course_models.Module).filter(
        course_models.Module.id == module_id
    ).first()
    
    if not db_module:
        raise HTTPException(status_code=404, detail="module not found")
    
    db_course = course_crud.get_course(db, db_module.course_id)
    if str(db_course.instructor_id) != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="unauthorized")
    
    return course_crud.create_lesson(db, lesson)

@router.get("/courses/search", response_model=List[course_schemas.CourseOut])
def search_courses(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    instructor_id: Optional[uuid.UUID] = Query(None),
    is_published: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    filters = course_schemas.CourseFilter(
        search=search,
        category=category,
        instructor_id=instructor_id,
        is_published=is_published
    )
    return search_courses(db, filters)
    
