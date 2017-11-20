# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from celery import shared_task
from python_metrics_client.influx import send_data as actual_send_data
from python_metrics_client.metrics_client import send_metric as actual_send_metric, send_product_metric as actual_send_product_metric

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_data(self, measurement, tags, value, timestamp=None, url=None, timeout=None):

    if not url:
        url = self.app.conf.python_metrics_client_url

    if not timeout:
        timeout = self.app.conf.python_metrics_client_timeout

    actual_send_data(url, measurement, tags, value, timestamp, timeout=timeout)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_metric(self, metric, value, tags, timestamp=None, environment=None, server=None, port=None):

    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    if not environment:
        environment = self.app.conf.metrics_environment

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_user

    actual_send_metric(server, port, metric, value, tags, timestamp, environment, client_type, username, password)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_product_metric(self, product, metric, value, tags, timestamp=None, environment=None, server=None, port=None):
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    if not environment:
        environment = self.app.conf.metrics_environment

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_user

    actual_send_product_metric(server, port, product, metric, value, tags, timestamp=timestamp,
                               username=username, password=password, environment=environment, client_type=client_type)
