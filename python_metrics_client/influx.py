# -*- coding: utf-8 -*-
import logging
import os
import time
import six
from datetime import datetime

import requests
from influxdb import InfluxDBClient

from python_metrics_client.exceptions import BadRequest

DEFAULT_TIMEOUT_IN_SECONDS = 30

logger = logging.getLogger(__name__)


def _convert_timestamp(timestamp):
    """Convert a given timestamp into the proper format accepted by influxdb client.

    Args:
        timestamp (Union[datetime,str,unicode,int]): a timestamp can be a
            datetime instance, a str or unicode value, or an integer.
    Returns:
        str: properly formatted timestamp

    """

    if not timestamp:
        timestamp = datetime.utcnow()

    if isinstance(timestamp, datetime):
        return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    elif isinstance(timestamp, six.string_types):
        return timestamp
    else:
        logger.info('%s is not a valid timestamp type', type(timestamp))
        raise TypeError


def send_data(url, measurement, tags, value, timestamp=None, timeout=None):
    """Send data point, using line protocol, to influxdb host.

    Args:
        url (str): influxdb address.
        measurement (str): metric name in influxdb.
        tags (dict): tags associated with this measure.
        value (Any): value measured for this metric.
        timestamp (Optional[Union[datetime,str,unicode,int]]): when this measure was taken.
        timeout (Optional[Union[int, float]): request timeout.

    Returns:
        bool: indicating if the line was sent to influxdb

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
        logger.warn('[send_data] problably not send timestamp in microseconds [%s]', timestamp)

    if not timeout:
        timeout = DEFAULT_TIMEOUT_IN_SECONDS

    data = "{},{} value={} {}".format(measurement, tags, value, int(timestamp))

    logger.debug("[send_data] url: %s data: %s", url, data)
    response = requests.post(url, data=data, timeout=timeout)

    if response.status_code != 204:
        logger.error('[send_data] bad request: %s %s', response.status_code, response.text)
        raise BadRequest('Error {} - {}'.format(response.status_code, response.text))

    logger.info('[send_data] success response status_code: {}'.format(response.status_code, response.text))

    return True


def send_metric(server, username, password, port, environment, metric, value, fields=None, tags=None, timestamp=None):
    """Send metric to influxdb.

    Args:
        server (str): metric server domain name
        username (str): username to access metric server
        password (str): password to access metric server
        port (int): metric server port
        environment (str): current environment (dev, stage, production)
        metric (str): measurement in metric server
        value (Union[int, float]): metric value
        fields (Optional[list]): additional fields in the form:
            [{'key1': value1},...,{'keyN': valueN}] (only supported by InfluxDB)
        tags (Optional[list]): list of tags in the form:
            [{'key1': value1},...,{'keyN': valueN}]
        timestamp (Optional[Union[datetime,str,unicode,int]]): time when this
            metric was collected.

    Returns:
        bool: indicating if the point was written

    """
    # In python3, celery converts datetime to a string.

    str_timestamp = _convert_timestamp(timestamp)

    data = [{
        'measurement': metric,
        'time': str_timestamp,
        'fields': {
            'value': value
        },
        'tags': {
            'environment': environment
        }
    }]

    for tag in (tags or []):
        data[0]['tags'].update(tag)

    for field in (fields or []):
        data[0]['fields'].update(field)

    logger.debug('influxdb send metric: data %s, tags %s', data, tags)

    client = InfluxDBClient(server, int(port), username, password, os.environ.get('INFLUX_DATABASE', 'metrics'))
    return client.write_points(data)
