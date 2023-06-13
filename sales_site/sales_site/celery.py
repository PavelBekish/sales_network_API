import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_site.settings')

app = Celery('sales_site')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'increase-debt-every-30-minutes': {
        'task': 'sales_network.tasks.increase_debt',
        'schedule': crontab(minute='*/30'),
    },
    'reduce-debt-every-day': {
        'task': 'sales_network.tasks.reduce_debt',
        'schedule': crontab(minute='30', hour='6'),
    },
}
