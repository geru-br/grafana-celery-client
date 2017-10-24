# -*- coding: utf-8 -*-
from celery import current_app


def includeme(settings):

    current_app.conf.python_metrics_client_url = settings.registry.settings.get('python_metrics_client.url')
    current_app.conf.python_metrics_client_timeout = settings.registry.settings.get('python_metrics_client.timeout', 30)

    current_app.conf.metrics_server = settings.registry.settings.get('metrics_server', 'influxdb.tick-prod.geroo.com.br')
    current_app.conf.metrics_client_protocol = settings.registry.settings.get('metrics_client_protocol', 'https')
    current_app.conf.metrics_client_port = settings.registry.settings.get('metrics_client_port', 8086)
    current_app.conf.metrics_client_timeout = settings.registry.settings.get('metrics_client_timeout', 30)
    current_app.conf.metrics_client_type = settings.registry.settings.get('metrics_client_type', 'influxdb')
    current_app.conf.metrics_user = settings.registry.settings.get('metrics_client_type', 'root')
    current_app.conf.metrics_password = settings.registry.settings.get('metrics_client_type', 'root')

    settings.scan()
