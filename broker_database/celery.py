import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broker_database.settings')

celery = Celery('broker_database')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()