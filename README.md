# Grafana celery client
=======================

This lib should be used by pyramid. It can be used standalone. :-)

Integration with Pyramid

Instalation

Add to project requirements.txt

```shell
...
-e git+https://github.com/geru-br/grafana-celery-client@master8#egg=grafana_celery_client
...

```

Add to project __init__.py or main() method

```python
	...
    settings['grafana_celery_client.url'] = get_from_env_or_settings(
        'grafana_celery_client.url', settings,
        default='http://52.91.126.40:8086/write?db=graphite'
    )

    ...
    config.include('grafana_celery_client')


Standalone


Tests

