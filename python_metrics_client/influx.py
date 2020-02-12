# -*- coding: utf-8 -*-
import logging
import os
import time
import requests

from influxdb import InfluxDBClient
from datetime import datetime
from python_metrics_client.exceptions import BadRequest

logger = logging.getLogger(__name__)


def _convert_timestamp(timestamp):
    '''
    :param timestamp: datetime with the timestamp date and time or str in the appropriate format
    :return: string with the corresponding date and time
    '''

    if not timestamp:
        timestamp = datetime.utcnow()

    if type(timestamp) is datetime:
        return timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif type(timestamp) is str:
        return timestamp
    elif type(timestamp) is unicode:
        return timestamp
    else:
        logger.info('{} is not a valid timestamp type'.format(type(timestamp)))
        raise TypeError


def send_data(url, measurement, tags, value, timestamp=None, timeout=None):
    """
    """
    if isinstance(tags, dict):

        ntags = []

        for k, v in tags.items():
            ntags.append('{}={}'.format(k, v))

        tags = ",".join(ntags)

    if not timestamp:
        timestamp = time.time() * 1000000000

    if float(timestamp) < time.time() * 1000000:
        # warn probably not send timestamp in microseconds
        logger.warn('send_data: problably not send timestamp in microseconds [{}]'.format(timestamp))

    if not timeout:
        timeout = 30

    data = "{},{} value={} {}".format(measurement, tags, value, int(timestamp))

    logger.info("[influx send data] url: {} data: {}".format(url, data))
    response = requests.post(url, data=data, timeout=timeout)

    if response.status_code != 204:
        logger.error('bad request: {} {}'.format(response.status_code, response.text))
        raise BadRequest('Error {} - {}'.format(response.status_code, response.text))

    logger.info('[influx send data] - success response status_code: {}'.format(response.status_code, response.text))


def send_metric(server, username, password, port, environment, metric, value, fields=None, tags=None, timestamp=None):
    '''
    Send metric to influxdb
    :param server: metric server domain name
    :param port: metric server port
    :param environment: current environment (dev, stage, production)
    :param metric: metric name
    :param value: metric value
    :param fields: Additional fileds in the form [{'key1': value1},...,{'keyN': valueN}] (only supported by InfluxDB)
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: datetime with metric time
    :return:
    '''

    # In python3, celery converts datetime to a string.

    str_timestamp = _convert_timestamp(timestamp)

    data = [
                {
                    'measurement': metric,
                    'time': str_timestamp,
                    'fields': {
                        'value': value
                    },
                    'tags': {
                        'environment': environment
                    }
                }
           ]

    for tag in (tags or []):
        data[0]['tags'].update(tag)

    for field in (fields or []):
        data[0]['fields'].update(field)

    logger.info('influxdb send metric: data: {}, tags: {}, server: {} port: {} username: {}'.format(data, tags, server, port, username))

    client = InfluxDBClient(server, int(port), username, password, os.environ.get('INFLUX_DATABASE', 'metrics'))
    client.write_points(data)
