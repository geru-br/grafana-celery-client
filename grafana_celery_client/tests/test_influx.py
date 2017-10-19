# -*- coding: utf-8 -*-

import mock
from base import TestCase
from influxdb import InfluxDBClient
from datetime import datetime
from grafana_celery_client.influx import send_metric as send_metric_influx


class InfluxTest(TestCase):

    @mock.patch.object(InfluxDBClient, 'write_points')
    def test_send_metric_with_time(self, influx_write):

        timestamp = datetime(2017, 10, 19, 18, 12, 51)
        data = [
                    {
                        'fields': {
                            'value': 10
                        },
                        'time': '2017-10-19T18:12:51Z',
                        'tags': {
                            'environment': 'dev',
                            'product': 'consignado'
                        },
                        'measurement': 'test'
                    }
                ]

        send_metric_influx('localhost', 8086, 'dev', 'test', 10, tags=[{'product': 'consignado'}], timestamp=timestamp)

        influx_write.assert_called_with(data)

    @mock.patch.object(InfluxDBClient, 'write_points')
    def test_send_metric_with_no_tags(self, influx_write):

        timestamp = datetime(2017, 10, 19, 18, 12, 51)
        data = [
                    {
                        'fields': {
                            'value': 10
                        },
                        'time': '2017-10-19T18:12:51Z',
                        'tags': {
                            'environment': 'dev'
                        },
                        'measurement': 'test'
                    }
                ]

        send_metric_influx('localhost', 8086, 'dev', 'test', 10, timestamp=timestamp)

        influx_write.assert_called_with(data)


