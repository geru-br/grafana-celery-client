import logging
import time
import six
import socket


logger = logging.getLogger(__name__)


def send_metric(server, port, tags, metric, value, timestamp=None):
    if not timestamp:
        timestamp = int(time.time())

    if tags :
        metric = '{}.{}.{}'
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(six.b("%s %f %d\n" % (metric, value, timestamp)))
    sock.close()
