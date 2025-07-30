from app.db.database import engine, Base
from app.db.models import Course

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created using SQLite!")
