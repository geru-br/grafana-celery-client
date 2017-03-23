

import mock
from base import TestCase
from grafana_celery_client.influx import send_data


class InfluxTest(TestCase):

    @mock.patch('grafana_celery_client.influx.requests')
    def test_tags_dict(self, celery_mock):
        send_data('url', 'measurement', {'tag': 'value'}, 2, 1490223248024070912)

        self.assertEquals(1, celery_mock.post.call_count)

        celery_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912')

    @mock.patch('grafana_celery_client.influx.requests')
    def test_tags_string(self, celery_mock):
        send_data('url', 'measurement', 'tag=value', 2, 1490223248024070912)

        self.assertEquals(1, celery_mock.post.call_count)
        celery_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912')

