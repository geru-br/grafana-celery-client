# -*- coding: utf-8 -*-
import click
from python_metrics_client.scripts.grafana import grafana
import logging
import sys


@click.group()
@click.option('-d', '--debug', envvar='DEGUG', default=None)
@click.option('-s', '--silent', default=None)
def cli(debug=True, silent=None):

    if not silent:

        root = logging.getLogger()

        if debug:
            root.setLevel(logging.DEBUG)
        else:
            root.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        root.addHandler(ch)


cli.add_command(grafana)

if __name__ == '__main__':
    cli()
