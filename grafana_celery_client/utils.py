
import time


def datetime_microsecond_timestamp(dt):

    return time.mktime(dt.utctimetuple()) * 1000000000
