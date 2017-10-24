import mock
from python_metrics_client.tests.base import TestCase
from datetime import datetime
from python_metrics_client.metrics_client import send_metric


class MetricsClientTest(TestCase):

    @mock.patch('python_metrics_client.metrics_client.send_metric_graphite')
    def test_send_metric_graphite(self, graphite_metric_mock):
        timestamp = datetime(2017, 10, 19, 18, 12, 51)
        send_metric('localhost', 2003, 'dev', 'test', 10, [{'product': 'consignado'}], timestamp=timestamp,
                    client_type='graphite')
        graphite_metric_mock.assert_called_with('localhost', 2003, 'dev', 'test', 10, [{'product': 'consignado'}],
                                                timestamp)

    @mock.patch('python_metrics_client.metrics_client.send_metric_influx')
    def test_send_metric_influx(self, influx_metric_mock):
        timestamp = datetime(2017, 10, 19, 18, 12, 51)
        send_metric('localhost', 8086, 'dev', 'test', 10, [{'product': 'consignado'}], timestamp=timestamp,
                    client_type='influxdb')
        influx_metric_mock.assert_called_with('localhost', 'root', 'root', 8086, 'dev', 'test', 10,
                                              [{'product': 'consignado'}], timestamp)


