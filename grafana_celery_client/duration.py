# -*- coding: utf-8 -*-
from timeit import default_timer as timer
from datetime import datetime
from tasks import send_metric


def timeit(func, environment, process_name=None, metric=None, tags=None, server=None, port=None):
    '''

    :param func: Decorated function
    :param environment: current environment (dev, stage, production)
    :param process_name: Name of the process that is being measured. If none is passed, the function name will be used
    :param metric: Metric name. If none is passed, duration will be used
    :param tags: list of tags in the form [{'key1': value1},...,{'keyN': valueN}]
    :param server: server domain name
    :param port:metric server port
    :return: This function will return whatever the decorated function returns
    '''

    if not process_name:
        process_name = func.__name__

    process_tag = {'process_name': process_name}

    if not tags:
        tags = [process_tag]
    else:
        tags.append(process_tag)

    if not metric:
        metric = 'duration'

    def wrapper():
        start = timer()
        ret = func()
        duration = timer() - start
        localtime = datetime.utcnow()
        send_metric.delay(environment, metric, duration, tags, localtime, server, port)
        return ret

    return wrapper
