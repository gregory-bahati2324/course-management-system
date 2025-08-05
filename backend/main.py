from fastapi import FastAPI
from app.api import courses
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="Course management system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["http://localhost:5500"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Management System API!"}

app.include_router(courses.router, prefix="/courses", tags=["courses"])

# gregory