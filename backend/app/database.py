from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .core.config import settings

# SQLAlchemy 2.x style base class
class Base(DeclarativeBase):
    pass


def get_sync_database_url(url: str) -> str:
    """Ensure database URL is compatible with synchronous create_engine."""
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


sync_db_url = get_sync_database_url(settings.database_url)

# Engine arguments based on database dialect
engine_kwargs = {"pool_pre_ping": True}
if "sqlite" in sync_db_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

engine = create_engine(
    sync_db_url,
    echo=settings.environment == "development" and settings.debug,
    **engine_kwargs,
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


# Database event listeners for connection setup
@event.listens_for(engine, "connect")
def set_pragma(dbapi_connection, connection_record):
    """Set database connection parameters."""
    if "sqlite" not in sync_db_url:
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("SET timezone = 'UTC'")
            cursor.close()
        except Exception:
            pass