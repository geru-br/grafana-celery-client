
import logging
import requests
import time

logger = logging.getLogger(__name__)


def send_data(url, measurement, tags, value, timestamp=None):
    """

    """
    if isinstance(tags, dict):

        ntags = []

        for k, v in tags.items():
            ntags.append('{}={}'.format(k, v))

        tags = ",".join(ntags)

    if not timestamp:
        timestamp = time.time() * 1000000000

    if timestamp < time.time() * 1000000:
        # warn problably not send timestamp in microseconds
        logger.warn('send_data: problably not send timestamp in microseconds [{}]'.format(timestamp))

    data = "{},{} value={} {}".format(measurement, tags, value, int(timestamp))

    logger.info("[grafana send data] url: {} data: {}".format(url, data))
    response = requests.post(url, data=data)
    logger.info(response.text)
