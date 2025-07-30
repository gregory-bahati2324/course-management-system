from fastapi import FastAPI
from app.api import courses

app = FastAPI(title="Course management system")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Management System API!"}

app.include_router(courses.router, prefix="/courses", tags=["courses"])

