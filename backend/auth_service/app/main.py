from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, user_service_user
from app.db.database import Base, engine
from app.db.user_database import Base as User_Base, engine as User_engine
from app.models import user # Ensure all models imported
from app.models import profile # Ensure all models imported

# Create all tables (for dev)
Base.metadata.create_all(bind=engine)
User_Base.metadata.create_all(bind=User_engine)

app = FastAPI(
    title="Auth Service",
    description="Handles user signin and signup",
    version="1.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user_service_user.router, prefix="/profile", tags=["profile"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
