# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from pyramid_transactional_celery import task_tm
from python_metrics_client.metrics_client import send_metric as actual_send_metric

logger = get_task_logger(__name__)


@task_tm(bind=True, queue='metrics_client')
def send_metric_tm(self, environment, metric, value, tags, timestamp=None, server=None, port=None):

    logger.info('Sending metric {}'.format(metric))
    if not server:
        server = self.app.conf.metrics_server

    if not port:
        port = self.app.conf.metrics_client_port

    client_type = self.app.conf.metrics_client_type

    actual_send_metric(server, port, environment, metric, value, tags, timestamp, client_type)