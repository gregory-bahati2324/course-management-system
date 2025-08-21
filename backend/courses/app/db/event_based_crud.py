from sqlalchemy.orm import Session
from datetime import datetime
from app.models import course_event_model
from app.db import course_event_schemas

def record_event(db: Session, event_data: course_event_schemas.LessonProgressEvent):
    progress = db.query(course_event_model.LessonProgress).filter_by(
        student_id=event_data.student_id,
        lesson_id=event_data.lesson_id
    ).first()
    
    if not progress:
        progress = course_event_model.LessonProgress(
            student_id=event_data.student_id,
            lesson_id=event_data.lesson_id,
            last_event=event_data.event
        )
        db.add(progress)
        
    progress.last_accessed = datetime.utcnow()
    progress.last_event = event_data.event
    
    # if the event is "completed", mark as completed
    if event_data.event.lower() == "completed":
        progress.is_completed = True   
        
    db.commit()
    db.refresh(progress)
    return progress     
