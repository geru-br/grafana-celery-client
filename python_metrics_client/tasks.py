# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from celery import shared_task
from python_metrics_client.influx import send_data as actual_send_data
from python_metrics_client.metrics_client import (
    send_metric as actual_send_metric,
    send_product_metric as actual_send_product_metric
)

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_data(self, measurement, tags, value, timestamp=None, url=None, timeout=None):
    if not self.app.conf.metrics_enabled:
        logger.debug('send_data: got config metrics_enabled == False, skipping.')
        return

    if not url:
        url = self.app.conf.python_metrics_client_url

    if not timeout:
        timeout = self.app.conf.python_metrics_client_timeout

    actual_send_data(url, measurement, tags, value, timestamp, timeout=timeout)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_metric(self, metric, value, fields=None, tags=None, timestamp=None, environment=None, server=None, port=None):
    """
    Send metric task. This will send a metric to time series DB with product tag

    :param self:
    :param metric: Metric name
    :param value: Value to be measured
    :param fields: Additional fileds in the form [{'key1': value1},...,{'keyN': valueN}] (only supported by InfluxDB)
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: timestamp in isoformat
    :param environment: current environment (dev, stage, production)
    :param server: metric server domain name
    :param port: metric server port
    :return:
    """
    if not self.app.conf.metrics_enabled:
        logger.debug('send_metric: got config metrics_enabled == False, skipping.')
        return

    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    if not environment:
        environment = self.app.conf.metrics_environment

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_password

    actual_send_metric(server, port, metric, value, fields=fields, tags=tags, timestamp=timestamp,
                       username=username, password=password, environment=environment, client_type=client_type)


@shared_task(bind=True, queue='metrics_client', time_limit=90, soft_time_limit=30)
def send_product_metric(self, product, metric, value, fields=None, tags=None,
                        timestamp=None, environment=None, server=None, port=None):
    """
    Send metric task. This will send a metric to time series DB

    :param self:
    :param product: Product name
    :param metric: Metric name
    :param value: Value to be measured
    :param fields: Additional fileds in the form [{'key1': value1},...,{'keyN': valueN}] (only supported by InfluxDB)
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: timestamp in isoformat
    :param environment: current environment (dev, stage, production)
    :param server: metric server domain name
    :param port: metric server port
    :return:
    """
    if not self.app.conf.metrics_enabled:
        logger.debug('send_product_metric: got config metrics_enabled == False, skipping.')
        return

    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    if not environment:
        environment = self.app.conf.metrics_environment

    username = self.app.conf.metrics_user
    password = self.app.conf.metrics_password

    actual_send_product_metric(server, port, product, metric, value, fields=fields, tags=tags, timestamp=timestamp,
                               username=username, password=password, environment=environment, client_type=client_type)
