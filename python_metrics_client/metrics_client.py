# -*- coding: utf-8 -*-
import logging

from datetime import datetime

from python_metrics_client.influx import send_metric as send_metric_influx
from python_metrics_client.graphite import send_metric as send_metric_graphite

logger = logging.getLogger(__name__)


def send_product_metric(server, port, product, metric, value, tags=None, timestamp=None,
                        environment=None, client_type='influxdb', username='root', password='root'):
    '''
    Send metric with product concept. Product key will be added as a tag for generic metric
    :param server: server domain name
    :param port: metric server port
    :param environment: current environment (dev, stage, production)
    :param product: product name
    :param metric: metric name
    :param value: metric value
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: datetime with metric time
    :param client_type: Type of metric collection egine (eg. 'graphite' or 'influxdb')
    :param username: Metric DB username if applicable
    :param password: Metric DB password if applicable
    :return:
    '''

    product_tag = {'product': product}

    if tags:
        tags.append({'product': product})
    else:
        tags = [product_tag]

    send_metric(server, port, environment, metric, value, tags, timestamp, client_type, username, password)


def send_metric(server, port,  metric, value, tags=None, timestamp=None, environment=None, client_type='influxdb',
                username='root', password='root'):
    '''
    Send metric generic metric
    :param server: server domain name
    :param port: metric server port
    :param environment: current environment (dev, stage, production)
    :param metric: metric name
    :param value: metric value
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: datetime with metric time
    :param client_type: Type of metric collection egine (eg. 'graphite' or 'influxdb')
    :param username: Metric DB username if applicable
    :param password: Metric DB password if applicable
    :return:
    '''
    if not timestamp:
        timestamp = datetime.utcnow()

    if client_type == 'influxdb':
        send_metric_influx(server, username, password, port, environment, metric, value, tags, timestamp)
    elif client_type == 'graphite':
        send_metric_graphite(server, port, environment, metric, value, tags, timestamp)
