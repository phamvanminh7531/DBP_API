from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# Đặt default settings module cho Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DBP_ml_api.settings')

app = Celery('DBP_ml_api')


# Sử dụng settings của Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động phát hiện các task trong apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
