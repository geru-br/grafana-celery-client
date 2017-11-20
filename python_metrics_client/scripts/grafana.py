# -*- coding: utf-8 -*-


import click
import json


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

    tags = json.loads(tags)

    sd(url, measurement, tags, value, timestamp=timestamp)


@grafana.group()
def tasks():
    pass


@tasks.command(name='send-data')
@click.argument('measurement')
@click.argument('tags')
@click.argument('value')
@click.option('-u', '--url', default=None)
@click.option('-t', '--timestamp', default=None)
def tasks_send_data(measurement, tags, value, url=None, timestamp=None):

    from python_metrics_client.tasks import send_data as sd

    tags = json.loads(tags)

    sd.delay(measurement, tags, value)


@tasks.command(name='send-metric')
@click.argument('metric')
@click.argument('tags')
@click.argument('value')
@click.option('-u', '--url', default=None)
@click.option('-t', '--timestamp', default=None)
def tasks_send_metric(metric, tags, value, url=None, timestamp=None):

    from python_metrics_client.tasks import send_metric as sm

    tags = json.loads(tags)

    sm.delay(metric, value, tags)
