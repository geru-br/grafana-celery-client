
from celery import shared_task

from grafana_celery_client.influx import send_data as actual_send_data


@shared_task(bind=True, queue='grafana_celery_client')
def send_data(self, dimension, tags, value, timestamp=None, url=None):

    # from celery.contrib import rdb; rdb.set_trace()

    if not url:
        url = self.app.conf.grafana_celery_client_url

    actual_send_data(url, dimension, tags, value, timestamp)
