
import logging
from celery import shared_task

from grafana_celery_client.influx import send_data as actual_send_data

logger = logging.getLogger(__name__)


@shared_task(bind=True, queue='grafana_celery_client')
def send_data(self, measurement, tags, value, timestamp=None, url=None, timeout=None):

    # from celery.contrib import rdb; rdb.set_trace()

    if not url:
        url = self.app.conf.grafana_celery_client_url

    if not timeout:
        timeout = self.app.conf.grafana_celery_client_timeout

    actual_send_data(url, measurement, tags, value, timestamp, timeout=timeout,
                     username=self.app.conf.grafana_celery_client_username,
                     password=self.app.conf.grafana_celery_client_password)
