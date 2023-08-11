from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ne_kidaem.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_daily_post_digest": {
        "task": "core.tasks.send_daily_post_digest",
        "schedule": crontab(hour=0, minute=0),
    },
}
