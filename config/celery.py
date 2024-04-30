import os

from celery import Celery
from decouple import config
from django.conf import settings

setting: str = (
    os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.development")
    if config("DEBUG", cast=bool)
    else "config.settings.production"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting)

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.task(bind=True, ignore_result=True)
