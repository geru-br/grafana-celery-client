# -*- coding: utf-8 -*-
from timeit import default_timer as timer
from datetime import datetime
from tasks import send_metric


def timeit(func, environment, metric=None, tags=None, server=None, port=None ):
    def wrapper():
        start = timer()
        ret = func()
        duration = timer() - start
        localtime = datetime.utcnow()

        send_metric.delay(environment, metric, duration, tags, localtime, server, port)
        return ret

    return wrapper
