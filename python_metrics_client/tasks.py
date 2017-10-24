# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from celery import shared_task
from pyramid_transactional_celery import task_tm
from python_metrics_client.influx import send_data as actual_send_data
from python_metrics_client.metrics_client import send_metric as actual_send_metric, send_product_metric

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='metrics_client')
def send_data(self, measurement, tags, value, timestamp=None, url=None, timeout=None):

    # from celery.contrib import rdb; rdb.set_trace()

    if not url:
        url = self.app.conf.python_metrics_client_url

    if not timeout:
        timeout = self.app.conf.python_metrics_client_timeout

    actual_send_data(url, measurement, tags, value, timestamp, timeout=timeout)


@shared_task(bind=True, queue='metrics_client')
def send_metric(self, environment, metric, value, tags, timestamp=None, server=None, port=None):

    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_user

    actual_send_metric(server, port, environment, metric, value, tags, timestamp, client_type, username, password)


@shared_task(bind=True, queue='metrics_client')
def send_product_metric(self, environment, product, metric, value, tags, timestamp=None, server=None, port=None):
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_user

    send_product_metric(server, port, environment, product,  metric, value, tags, timestamp, client_type,
                        username, password)


@task_tm(bind=True, queue='metrics_client')
def send_metric_tm(self, environment, metric, value, tags, timestamp=None, server=None, port=None):

    logger.info('Sending metric {}'.format(metric))
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    actual_send_metric(server, port, environment, metric, value, tags, timestamp, client_type)
