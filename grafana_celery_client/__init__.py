from celery import current_app


def includeme(settings):
    #
    # current_app.conf.grafana_celery_client_url = settings.registry.settings.get('grafana_celery_client.url')
    #
    # current_app.conf.grafana_celery_client_timeout = settings.registry.settings.get('grafana_celery_client.timeout', 30)

    current_app.conf.metrics_server = settings.registry.settings.get('metrics_server', 'graphite.geru.com.br')
    current_app.conf.metrics_client_protocol = settings.registry.settings.get('metrics_client_protocol', 'https')
    current_app.conf.metrics_client_port = settings.registry.settings.get('metrics_client_port', 2003)
    current_app.conf.metrics_client_timeout = settings.registry.settings.get('metrics_client_timeout', 30)
    current_app.conf.metrics_client_type = settings.registry.settings.get('metrics_client_type', 'influxdb')

    settings.scan()
