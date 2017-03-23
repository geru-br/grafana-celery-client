from celery import current_app


def includeme(settings):

    current_app.conf.grafana_celery_client_url = settings.registry.settings.get('grafana_celery_client.url')

    current_app.conf.grafana_celery_client_timeout = settings.registry.settings.get('grafana_celery_client.timeout', 30)

    settings.scan()
