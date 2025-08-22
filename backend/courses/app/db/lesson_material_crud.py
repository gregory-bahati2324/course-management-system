import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
import uuid
from pathlib import Path
import shutil
from datetime import datetime
from app.models.file_upload_model import LessonMaterial
from app.models.course_models import Lesson

UPLOAD_DIR = "app/uploads/lessons/"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_lesson_material(db: Session, lesson_id: str, files: list[UploadFile]):
    saved_files = []
    for file in files:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        material = LessonMaterial(
            lesson_id=lesson_id,
            filename=file.filename,
            file_url=file_path,
            uploaded_at=datetime.utcnow()
        )
        db.add(material)
        saved_files.append(material)
        
    db.commit()
    db.refresh(saved_files[0])
    return saved_files    

#get lesson materials
def get_lesson_materials(db: Session, lesson_id: str):
    return db.query(LessonMaterial).filter(LessonMaterial.lesson_id == lesson_id).all()

#get lesson material by id
def get_lesson_material_by_id(db: Session, material_id: str):
    return db.query(LessonMaterial).filter(LessonMaterial.id == material_id).first()

def get_lesson_details(db: Session, lesson_id: str):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson:
        lesson.materials = db.query(LessonMaterial).filter(LessonMaterial.lesson_id == lesson_id).all()
    return lesson
    