# -*- coding: utf-8 -*-
from timeit import default_timer as timer
from datetime import datetime
from celery import shared_task
import functools

from celery.utils.log import get_task_logger
from python_metrics_client.metrics_client import send_metric as actual_send_metric

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='metrics_client')
def _send_metric(self, environment, metric, value, tags, timestamp=None, server=None, port=None):
    '''
    This task should only be used by the timeit decorator
    '''
    if not self.app.conf.metrics_enabled:
        logger.info('_send_metric: got config metrics_enabled == False, skipping.')
        return

    logger.info('Sending metric {}'.format(metric))
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    if not environment:
        environment = self.app.conf.metrics_environment

    client_type = self.app.conf.metrics_client_type

    actual_send_metric(
        server=server, port=port, metric=metric, value=value, tags=tags, timestamp=timestamp,
        environment=environment, client_type=client_type
    )


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
                _tags = (_process_tag,)
            else:
                # Using tuple to avoid issues with mututable objects (e.g. lists)
                # See issue: https://github.com/geru-br/python-metrics-client/issues/9
                _tags = tuple(tag for tag in _tags) + (_process_tag,)

            if not _metric:
                _metric = 'duration'

            start = timer()
            ret = func(*args, **kwargs)
            duration = timer() - start
            localtime = datetime.utcnow().isoformat()
            _send_metric.delay(environment, _metric, duration, list(_tags), localtime, server, port)
            return ret

        return wrapper
    return _timeit
