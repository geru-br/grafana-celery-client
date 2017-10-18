
import logging
from celery import shared_task

from grafana_celery_client.influx import send_metric as send_metric_influx
from grafana_celery_client.graphite import send_metric as send_metric_graphite

logger = logging.getLogger(__name__)


# @shared_task(bind=True, queue='grafana_celery_client')
# def send_data(self, measurement, tags, value, timestamp=None, url=None, timeout=None):
#
#     # from celery.contrib import rdb; rdb.set_trace()
#
#     if not url:
#         url = self.app.conf.grafana_celery_client_url
#
#     if not timeout:
#         timeout = self.app.conf.grafana_celery_client_timeout
#
#     # actual_send_data(url, measurement, tags, value, timestamp, timeout=timeout)


@shared_task(bind=True, queue='metrics_client')
def send_metric(self, product, environment, metric, value, timestamp=None, server=None, port=None):

    if not server:
        server = self.app.conf.graphite_client_server

    if not port:
        port = self.app.conf.graphite_client_metric_port

    if self.app.metrics_client_type == 'influxdb':
        send_metric_influx(server, port, metric, value, timestamp)
    elif self.app.metrics_client_type == 'graphite':
        send_metric_graphite(server, port, metric, value, timestamp)

