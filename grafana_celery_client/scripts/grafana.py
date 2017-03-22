# -*- coding: utf-8 -*-


import click


@click.group()
def grafana():
    pass


@grafana.group()
def influx():
    pass


@influx.command(name='send')
@click.argument('url')
@click.argument('dimension')
@click.argument('tags')
@click.argument('value')
def influx_send_data(url, dimension, tags, value):

    from grafana_celery_client.influx import send_data as sd

    sd(url, dimension, tags, value)


@grafana.group()
def tasks():
    pass


@tasks.command(name='send')
@click.argument('dimension')
@click.argument('tags')
@click.argument('value')
@click.option('-u', '--url', default=None)
def tasks_send_data(dimension, tags, value, url):

    from grafana_celery_client.tasks import send_data as sd

    sd.delay(dimension, tags, value)