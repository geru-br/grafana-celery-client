# -*- coding: utf-8 -*-
import logging

from celery import current_app


logger = logging.getLogger(__name__)


def includeme(config):

    current_app.conf.python_metrics_client_url = config.registry.settings.get('python_metrics_client.url')
    current_app.conf.python_metrics_client_timeout = config.registry.settings.get('python_metrics_client.timeout', 30)

    current_app.conf.metrics_enabled = config.registry.settings.get('metrics_enabled', True)

    current_app.conf.metrics_server = config.registry.settings.get('metrics_server', 'influxdb.tick-prod.geroo.com.br')
    current_app.conf.metrics_client_protocol = config.registry.settings.get('metrics_client_protocol', 'https')
    current_app.conf.metrics_client_port = config.registry.settings.get('metrics_client_port', 8086)
    current_app.conf.metrics_client_timeout = config.registry.settings.get('metrics_client_timeout', 30)
    current_app.conf.metrics_client_type = config.registry.settings.get('metrics_client_type', 'influxdb')
    current_app.conf.metrics_user = config.registry.settings.get('metrics_user', 'root')
    current_app.conf.metrics_password = config.registry.settings.get('metrics_password', 'root')
    current_app.conf.metrics_environment = config.registry.settings.get('metrics_environment', 'production')

    logger.info('metrics-client config: server: {}://{}:{}'.format(
        current_app.conf.metrics_client_protocol,
        current_app.conf.python_metrics_client_url,
        current_app.conf.metrics_client_port
    ))

    logger.info('metrics-client config: client: {} - {}'.format(
        current_app.conf.metrics_client_type,
        current_app.conf.metrics_environment
    ))

    config.scan()
