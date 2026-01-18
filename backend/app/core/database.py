from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Construct the Database URL. 
# Defaults to a local postgres container if not set, or uses the Supabase connection string.
# Note: Pydantic settings will have already loaded this from .env if present.
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# If using Supabase directly via connection pooling (port 6543/5432), the URL format in .env should be prioritized.
# If SUPABASE_URL is provided in a specific format, we might want to use that directly.
# For MVP, we stick to the component-based construction from config.py settings.

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # 'pool_pre_ping' sends a test query (SELECT 1) to ensure connection is alive before handing out session
    pool_pre_ping=True 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency generator for FastAPI. 
    Yields a database session and ensures it closes after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
