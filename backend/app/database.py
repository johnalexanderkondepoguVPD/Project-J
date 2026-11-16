from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .core.config import settings

# SQLAlchemy 2.x style base class
class Base(DeclarativeBase):
    pass

# Create engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.environment == "development",
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get DB session
def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database event listeners for pgvector optimization
@event.listens_for(engine, "connect")
def set_pragma(dbapi_connection, connection_record):
    """Set database connection parameters."""
    cursor = dbapi_connection.cursor()
    cursor.execute("SET timezone = 'UTC'")
    cursor.close()