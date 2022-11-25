import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payment.settings")


app = Celery("payment", broker="redis://redis:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
