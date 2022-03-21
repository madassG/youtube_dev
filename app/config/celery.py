import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-users-every-24-hours': {
        'task': 'channels.tasks.check_accounts',
        'schedule': crontab(hour="*/24"),
    },
    'check-videos-every-24-hours': {
        'task': 'channels.tasks.check_videos',
        'schedule': crontab(hour="*/12"),
    },
    'check-date-publish': {
        'task': 'bot.tasks.check_publish',
        'schedule': crontab(hour="*/12"),
    }
}

