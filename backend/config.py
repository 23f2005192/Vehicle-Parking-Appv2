from celery.schedules import crontab

beat_schedule = {
    'send-monthly-reports': {
        'task': 'tasks.send_all_monthly_reports',
        'schedule': crontab(minute='*/2', hour='*'),  # Every 2 minutes
    },
}
