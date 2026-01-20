# app/init_db.py

from app.models.database import Base, engine
from app.models.tables import ScanRecord  # make sure this import is correct

print("📀 Initializing database...")
Base.metadata.create_all(bind=engine)
print("✅ Database initialized.")