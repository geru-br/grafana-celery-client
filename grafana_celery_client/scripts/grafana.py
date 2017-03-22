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
def send_data(url, dimension, tags, value):

    from grafana_celery_client.influx import send_data as sd

    sd(url, dimension, tags, value)