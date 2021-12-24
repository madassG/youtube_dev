import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtubedev.settings')

app = Celery('youtubecheck')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-users-every-24-hours': {
        'task': 'channels.tasks.check_accounts',
        'schedule': crontab(minute=1),
    },
    'check-videos-every-24-hours': {
        'task': 'channels.tasks.check_videos',
        'schedule': crontab(minute=1),
    },
    'check-date-publish': {
        'task': 'bot.tasks.check_publish',
        'schedule': crontab(minute=1),
    }
}

