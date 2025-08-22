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
        course_id=str(enrollment.course_id),
        student_id=str(enrollment.student_id)
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

def create_lesson(
    db: Session, 
    lesson: course_schemas.LessonCreate, 
    module_id: str
) -> course_schemas.LessonOut:
    db_lesson = course_models.Lesson(
        title=lesson.title,
        content=lesson.content,
        duration_days=lesson.duration_days,
        position=lesson.position,
        video_url=lesson.video_url,
        document_url=lesson.document_url,
        module_id=module_id   # ✅ use the path param, not lesson.module_id
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return course_schemas.LessonOut.from_orm(db_lesson)

# Get a lesson by ID
def get_lesson(db: Session, lesson_id: str) -> course_models.Lesson:
    return db.query(course_models.Lesson).filter(
        course_models.Lesson.id == lesson_id
    ).first()


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

def get_course(db: Session, course_id: str) -> course_models.Course:
    """Retrive a single course by id"""
    return db.query(course_models.Course).filter(
        course_models.Course.id == course_id
    ).first()      
    
def mark_lesson_complete(db: Session, progress: course_schemas.LessonProgressCreate) -> course_schemas.LessonProgressOut:
    db_progress = course_models.LessonProgress(
        lesson_id=str(progress.lesson_id),
        student_id=progress.student_id,
        progress_percentage=100  # Assuming completion means 100% progress
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_lesson_progress(db: Session, lesson_id: str, student_id: str) -> course_models.LessonProgress:
    return db.query(course_models.LessonProgress).filter(
        course_models.LessonProgress.lesson_id == lesson_id,
        course_models.LessonProgress.student_id == student_id
    ).first()
    
   
def get_course_progress(db: Session, course_id: str, student_id: str):
    """Get all lesson progress for a specific course and student"""
    lesson = db.query(course_models.Lesson).filter_by(
        module_id=course_id
    ).all()
    completed_lessons = db.query(course_models.LessonProgress).filter_by(
        student_id=student_id
    ).join(course_models.Lesson).filter(course_models.Lesson.module_id == course_id).all()
    
    return {
        "total_lessons": len(lesson),
        "completed_lessons": len(completed_lessons),
        "is_course_completed": len(lesson) > 0 and len(completed_lessons) == len(lesson),
        "progress_percentage": (len(completed_lessons) / len(lesson)) * 100 if lesson else 0}