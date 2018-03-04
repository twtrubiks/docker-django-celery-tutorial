from datetime import timedelta

from celery.schedules import crontab

# Timezone
timezone = 'Asia/Taipei'

# import
imports = (
    'celery_app.tasks',
)

# result
result_backend = 'db+sqlite:///results.sqlite'

# schedules
beat_schedule = {
    'every-2-seconds': {
        'task': 'celery_app.tasks.add',
        'schedule': timedelta(seconds=2),
        'args': (5, 8)
    },
    'specified-time': {
        'task': 'celery_app.tasks.add',
        'schedule': crontab(hour=8, minute=50),
        'args': (50, 50)
    }

}
