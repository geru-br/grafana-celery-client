# -*- coding: utf-8 -*-
import logging
import time
import six
import socket
from datetime import datetime


logger = logging.getLogger(__name__)


def _convert_timestamp(timestamp):
    '''
    :param timestamp: datetime with the timestamp date and time or str in the appropriate format
    :return: string with the corresponding date and time
    '''

    if not timestamp:
        return int(time.time())
    elif type(timestamp) is datetime:
        return time.mktime(timestamp.timetuple())
    elif type(timestamp) is str:
        _datetime = datetime.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')
        return int(time.mktime(_datetime.timetuple()))
    elif type(timestamp) is unicode:
        _datetime = datetime.strptime(timestamp[0:19], '%Y-%m-%dT%H:%M:%S')
        return int(time.mktime(_datetime.timetuple()))
    else:
        logger.info('%s is not a valid timestamp type', type(timestamp))
        raise TypeError


def send_metric(server, port, environment, metric, value, tags=None, timestamp=None):
    '''
    Send metric to graphite
    :param server: server domain name
    :param port: metric server port
    :param environment: current environment (dev, stage, production)
    :param metric: metric name
    :param value: metric value
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param timestamp: datetime with metric time
    :return:
    '''

    # In python3, celery converts datetime to a string.
    ts = _convert_timestamp(timestamp)

    metric_path = environment + '.'

    if tags:
        for tag in tags:
            for item in tag.items():
                metric_path += item[1] + '.'

    metric_path += metric

    sock = socket.socket()
    sock.connect((server, int(port)))
    sock.send(six.b("%s %f %d\n" % (metric_path, value, ts)))
    sock.close()
