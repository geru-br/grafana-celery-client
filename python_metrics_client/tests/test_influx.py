# -*- coding: utf-8 -*-

import mock
from python_metrics_client.tests.base import TestCase
from influxdb import InfluxDBClient
from datetime import datetime
from python_metrics_client.influx import send_metric as send_metric_influx
from python_metrics_client.influx import send_data
from python_metrics_client.exceptions import BadRequest


class InfluxTest(TestCase):
    @mock.patch('python_metrics_client.influx.requests')
    def test_tags_dict(self, requests_mock):
        mocked_response = mock.Mock()
        requests_mock.post.return_value = mocked_response
        mocked_response.status_code = 204

        send_data('url', 'measurement', {'tag': 'value'}, 2, 1490223248024070912)

        self.assertEquals(1, requests_mock.post.call_count)

        requests_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912',
                                              timeout=30)

    @mock.patch('python_metrics_client.influx.requests')
    def test_tags_string(self, requests_mock):
        mocked_response = mock.Mock()
        requests_mock.post.return_value = mocked_response
        mocked_response.status_code = 204

        send_data('url', 'measurement', 'tag=value', 2, 1490223248024070912)

        self.assertEquals(1, requests_mock.post.call_count)
        requests_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912',
                                              timeout=30)

    @mock.patch('python_metrics_client.influx.requests')
    def test_bad_request_500(self, requests_mock):
        mocked_response = mock.Mock()
        requests_mock.post.return_value = mocked_response
        mocked_response.status_code = 500
        mocked_response.text = 'Error'

        self.assertRaises(BadRequest, send_data, 'url', 'measurement', 'tag=value', 2, 1490223248024070912)

    @mock.patch('python_metrics_client.influx.requests')
    def test_bad_request_400(self, requests_mock):
        mocked_response = mock.Mock()
        requests_mock.post.return_value = mocked_response
        mocked_response.status_code = 400
        mocked_response.text = 'Error'

        self.assertRaises(BadRequest, send_data, 'url', 'measurement', 'tag=value', 2, 1490223248024070912)

    @mock.patch.object(InfluxDBClient, 'write_points')
    def test_send_metric_with_time(self, influx_write):

        timestamp = datetime(2017, 10, 19, 18, 12, 51)
        data = [
                    {
                        'fields': {
                            'value': 10,
                            'add_field_1': 'a',
                            'add_field_2': 2
                        },
                        'time': '2017-10-19T18:12:51Z',
                        'tags': {
                            'environment': 'dev',
                            'product': 'consignado'
                        },
                        'measurement': 'test'
                    }
                ]

        send_metric_influx(
            'localhost', 'root', 'root',  8086, 'dev', 'test', 10,
            fields=[{'add_field_1': 'a'}, {'add_field_2': 2}], tags=[{'product': 'consignado'}], timestamp=timestamp
        )

        influx_write.assert_called_with(data)

    @mock.patch.object(InfluxDBClient, 'write_points')
    def test_send_metric_with_no_fields_or_tags(self, influx_write):

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

        send_metric_influx('localhost', 'root', 'root', 8086, 'dev', 'test', 10, timestamp=timestamp)

        influx_write.assert_called_with(data)
