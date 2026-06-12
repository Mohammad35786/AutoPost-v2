from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Adjust the database URL if it's async or needs a specific driver format
# For standard psycopg (psycopg 3), the URL should be postgresql+psycopg://...
# The prompt specified psycopg[binary] as the Postgres driver.
# Assuming standard postgresql:// URL, SQLAlchemy 2.0 with psycopg3 might require postgresql+psycopg://
# We'll stick to what user provides, if it starts with postgresql:// and fails we might need to adjust, 
# but SQLAlchemy 2.0 defaults to psycopg2 for postgresql://, so we might need postgresql+psycopg:// 
# if they are providing a standard postgresql:// URL. We can handle that in the engine creation or let the user adjust .env.
# Let's replace postgresql:// with postgresql+psycopg:// if needed, or just rely on the driver string.

db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
# SQLAlchemy 2.0 recommended for psycopg3 is postgresql+psycopg://
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
