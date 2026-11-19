import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    app_name: str = "Project-J"
    app_version: str = "0.1.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True") == "True"

    @property
    def APP_VERSION(self) -> str:
        return self.app_version
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = None

    def __post_init__(self):
        if self.cors_origins is None:
            cors_env = os.getenv("CORS_ORIGINS", "http://localhost:3000")
            self.cors_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/project_j")
    test_database_url: str = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/project_j_test")
    
    # Redis
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    
    # Security & Sessions
    secret_key: str = os.getenv("SECRET_KEY", "change-this-to-a-secure-random-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME", "project_j_session")
    session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    session_cookie_samesite: str = os.getenv("SESSION_COOKIE_SAMESITE", "lax")
    session_expire_days: int = int(os.getenv("SESSION_EXPIRE_DAYS", "7"))
    
    # AI / LLM
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Storage (S3-compatible)
    s3_endpoint_url: str = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")
    s3_access_key_id: str = os.getenv("S3_ACCESS_KEY_ID", "minio")
    s3_secret_access_key: str = os.getenv("S3_SECRET_ACCESS_KEY", "minio123")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "project-j")
    s3_region: str = os.getenv("S3_REGION", "us-east-1")
    
    # Scraping
    scraping_timeout: int = int(os.getenv("SCRAPING_TIMEOUT", "30"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # OCR
    paddle_ocr_url: str = os.getenv("PADDLE_OCR_URL", "http://localhost:8080")
    paddle_ocr_api_key: str = os.getenv("PADDLE_OCR_API_KEY", "")
    
    # Celery
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    celery_timezone: str = os.getenv("CELERY_TIMEZONE", "UTC")
    celery_beat_schedule_interval: int = int(os.getenv("CELERYBEAT_SCHEDULE_INTERVAL", "30"))

settings = Settings()