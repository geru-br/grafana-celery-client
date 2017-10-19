# -*- coding: utf-8 -*-
import logging
import time
import six
import socket


logger = logging.getLogger(__name__)


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

    if not timestamp:
        ts = int(time.time())
    else:
        ts = time.mktime(timestamp.timetuple())

    metric_path = environment + '.'

    if tags:
        for tag in tags:
            for item in tag.items():
                metric_path += item[1] + '.'

    metric_path += metric

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(six.b("%s %f %d\n" % (metric_path, value, ts)))
    sock.close()
