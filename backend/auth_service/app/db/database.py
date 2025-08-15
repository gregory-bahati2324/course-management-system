import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure DB file exists and is writable
DB_FILE = "test.db"
if not os.path.exists(DB_FILE):
    open(DB_FILE, "w").close()
os.chmod(DB_FILE, 0o666)

DATABASE_URL = f"sqlite:///./{DB_FILE}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
