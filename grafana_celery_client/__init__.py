from celery import current_app


def includeme(settings):

    current_app.conf.grafana_celery_client_url = settings.registry.settings.get('grafana_celery_client.url')

    settings.scan()

