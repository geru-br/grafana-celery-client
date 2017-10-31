# -*- coding: utf-8 -*-
from timeit import default_timer as timer
from datetime import datetime
from celery import task
import functools

import logging
from python_metrics_client.metrics_client import send_metric as actual_send_metric

logger = logging.getLogger(__name__)


@task(bind=True, queue='metrics_client')
def _send_metric(self, environment, metric, value, tags, timestamp=None, server=None, port=None):
    '''
    This task should only be used by the timeit decorator
    '''

    logger.info('Sending metric {}'.format(metric))
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    if not environment:
        environment = self.app.conf.metrics_environment

    client_type = self.app.conf.metrics_client_type

    actual_send_metric(server, port, metric, value, tags, timestamp, environment,  client_type)


def timeit(environment=None, process_name=None, metric=None, tags=None, server=None, port=None):
    '''
    :param environment: current environment (dev, stage, production)
    :param process_name: Name of the process that is being measured.
    :param metric: Metric name. If none is passed, duration will be used
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param server: server domain name
    :param port:metric server port
    :return: This function will return whatever the decorated function returns
    '''

    def _timeit(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _process_name = process_name
            _tags = tags
            _metric = metric

            if not _process_name:
                _process_name = func.__name__

            _process_tag = {'process_name': _process_name}

            if not _tags:
                _tags = [_process_tag]
            else:
                _tags.append(_process_tag)

            if not _metric:
                _metric = 'duration'

            start = timer()
            ret = func(*args, **kwargs)
            duration = timer() - start
            localtime = datetime.utcnow()
            _send_metric.delay(environment, _metric, duration, _tags, localtime, server, port)
            return ret

        return wrapper
    return _timeit
