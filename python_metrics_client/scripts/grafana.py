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
@click.argument('measurement')
@click.argument('tags')
@click.argument('value')
@click.option('-t', '--timestamp', default=None)
def influx_send_data(url, measurement, tags, value, timestamp=None):

    from python_metrics_client.influx import send_data as sd

    sd(url, measurement, tags, value, timestamp=timestamp)


@grafana.group()
def tasks():
    pass


@tasks.command(name='send')
@click.argument('measurement')
@click.argument('tags')
@click.argument('value')
@click.option('-u', '--url', default=None)
@click.option('-t', '--timestamp', default=None)
def tasks_send_data(measurement, tags, value, url=None, timestamp=None):

    from python_metrics_client.tasks import send_data as sd

    sd.delay(measurement, tags, value)


@grafana.command(name='send_metric')
@click.argument('path')
@click.argument('value')
@click.option('-t', '--timestamp', default=None)
def tasks_send_metric(path, value, timestamp=None):
    tasks.send_metric.delay(path, value, timestamp)
