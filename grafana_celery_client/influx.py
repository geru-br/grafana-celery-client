
import logging
import requests
import time

logger = logging.getLogger(__name__)


def send_data(url, measurement, tags, value, timestamp=None):
    """

    """
    if isinstance(tags, dict):

        ntags = []

        for key, value in tags.items():
            ntags.append('{}={}'.format(key, value))

        tags = ",".join(ntags)

    if not timestamp:
        timestamp = time.time() * 1000000000

    data = "{},{} value={} {}".format(measurement, tags, value, int(timestamp))

    logger.info("[grafana send data] url: {} data: {}".format(url, data))
    response = requests.post(url, data=data)
    logger.info(response.text)
