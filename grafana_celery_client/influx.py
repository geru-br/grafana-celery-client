
import logging
import requests
import time
from grafana_celery_client.exceptions import BadRequest

logger = logging.getLogger(__name__)


def send_data(url, measurement, tags, value, timestamp=None, timeout=None):
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

    if not timeout:
        timeout = 30

    data = "{},{} value={} {}".format(measurement, tags, value, int(timestamp))

    logger.info("[influx send data] url: {} data: {}".format(url, data))
    response = requests.post(url, data=data, timeout=timeout)

    if response.status_code != 204:
        raise BadRequest('Error {} - {}'.format(response.status_code, response.text))

    logger.info('[influx send data] - success response status_code: {}'.format(response.status_code, response.text))
