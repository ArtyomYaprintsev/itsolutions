import os

from celery import Celery


app = Celery(__name__)
app.conf.broker_url = os.environ.get(  # type: ignore
    'CELERY_BROKER_URL', 'redis://localhost:6379')
app.conf.result_backend = os.environ.get(  # type: ignore
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')
app.autodiscover_tasks(['server.tasks'])
