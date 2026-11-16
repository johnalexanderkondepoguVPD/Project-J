from celery import Celery
from .config import settings

def make_celery(app_name=None):
    """Create and configure a Celery application instance."""
    if app_name is None:
        app_name = settings.app_name
    
    celery = Celery(
        app_name,
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
        timezone=settings.celery_timezone,
    )
    
    # Update Celery configuration
    celery.conf.update(
        result_expires=3600,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        beat_schedule_interval=settings.celery_beat_schedule_interval,
    )
    
    return celery

# Create celery instance
celery_app = make_celery()