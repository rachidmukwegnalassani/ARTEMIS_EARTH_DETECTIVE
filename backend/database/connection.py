import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Récupération de la variable DATABASE_URL depuis Render/Supabase
DATABASE_URL = os.getenv("DATABASE_URL")

# Gestion si l'URL commence par postgres:// (correctif Render standard)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dépendance FastAPI pour obtenir une session de BDD propre"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()