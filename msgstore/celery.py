from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from msgstore.settings import TASK_PERIOD, DELTA
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msgstore.settings')

app = Celery('msgstore')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     'old-history-clean': {
#         'task': 'msgapp.tasks.clear_old_history',
#         'schedule': TASK_PERIOD * 24 * 60 * 60,      # time in seconds
#         'args': (DELTA, )                            # maximum time to store history in days
#     },
# }
