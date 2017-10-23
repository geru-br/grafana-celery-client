# -*- coding: utf-8 -*-
from timeit import default_timer as timer
from datetime import datetime
from tasks import send_metric
import functools


def timeit(environment, process_name, metric=None, tags=None, server=None, port=None):
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
            send_metric.delay(environment, _metric, duration, _tags, localtime, server, port)
            return ret

        return wrapper
    return _timeit
