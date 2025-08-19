from operator import or_
from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from app.models import course_models
from app.db import course_schemas

def create_course(db: Session, course: course_schemas.CourseCreate) -> course_schemas.CourseOut:
    db_course = course_models.Course(
        title=course.title,
        description=course.description,
        instructor_id=course.instructor_id,
        category=course.category,
        is_published=course.is_published
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return course_schemas.CourseOut.from_orm(db_course)

def create_enrollment(db: Session, enrollment: course_schemas.EnrollmentCreate) -> course_schemas.EnrollmentOut:
    db_enrollment = course_models.Enrollment(
        course_id=enrollment.course_id,
        student_id=enrollment.student_id
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return course_schemas.EnrollmentOut.from_orm(db_enrollment)

def create_module(db: Session, module: course_schemas.ModuleCreate) -> course_schemas.ModuleOut:
    db_module = course_models.Module(
        title=module.title,
        position=module.position,
        description=module.description,
        course_id=module.course_id
    )
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return course_schemas.ModuleOut.from_orm(db_module)

def create_lesson(db: Session, lesson: course_schemas.LessonCreate) -> course_schemas.LessonOut:
    db_lesson = course_models.Lesson(
        title=lesson.title,
        content=lesson.content,
        duration_days=lesson.duration_days,
        position=lesson.position,
        video_url=lesson.video_url,
        document_url=lesson.document_url,
        module_id=lesson.module_id
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return course_schemas.LessonOut.from_orm(db_lesson)

def search_courses(db: Session, filters: course_schemas.CourseFilter, limit: int = 100):
    query = db.query(course_models.Course)
    
    if filters.search:
        query = query.filter(
            or_(
                course_models.Course.title.ilike(f"%{filters.search}%"),
                course_models.Course.description.ilike(f"%{filters.search}%")
            )
        )
    if filters.category:
        query = query.filter(course_models.Course.category == filters.category)
        
    if filters.instructor_id:
        query = query.filter(course_models.Course.instructor_id == filters.instructor_id)
    if filters.is_published is not None:
        query = query.filter(course_models.Course.is_published == filters.is_published)
        
    return query.order_by(course_models.Course.created_at.desc()).limit(limit).all()     

def get_course(db: Session, course_id: UUID):
    """Retrive a single course by id"""
    return db.query(course_models.Course).filter(
        course_models.Course.id == course_id
    ).first()      