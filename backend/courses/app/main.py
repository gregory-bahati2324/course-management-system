from fastapi import FastAPI
from app.routes.courses import router
from app.db.course_database import Base, engine
from app.models import course_models  # make sure this import happens BEFORE create_all

# Force all models to be registered before creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Courses API",
    description="API for managing courses and enrollments",
    version="1.0.0",
)

app.include_router(router, prefix="/courses")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
