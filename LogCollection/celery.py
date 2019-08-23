from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery

# set the default Django settings module for the 'celery' program.
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LogCollection.settings')

app = Celery('LogCollection')
# this ‘demo’ is your project name !!!
# app.conf.timezone = 'UTC'




# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')



# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'assets.task.add',
#         'schedule': 10.0,
#         'args': (16, 16)
#     },
# }

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from celery.schedules import crontab

