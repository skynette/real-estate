from __future__ import absolute_import
import os

from celery import Celery
from zcore.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zcore.settings.development")

app = Celery("real_estate")

app.config_from_object("zcore.settings.development", namespace="CELLERY")

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)

