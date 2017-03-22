
import logging
import requests
import time

logger = logging.getLogger(__name__)


def send_data(url, dimension, tags, value, timestamp=None):

    if not timestamp:
        timestamp = time.time()

    data = "{},{} value={} {}".format(dimension, tags, value, int(timestamp))

    logger.info("[grafana send data] url: {} data: {}".format(url, data))
    response = requests.post(url, data=data)
    logger.info(response.text)

