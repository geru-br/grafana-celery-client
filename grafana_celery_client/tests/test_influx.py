

import mock
from base import TestCase
from grafana_celery_client.influx import send_data
from grafana_celery_client.exceptions import BadRequest


# class InfluxTest(TestCase):
#
#     @mock.patch('grafana_celery_client.influx.requests')
#     def test_tags_dict(self, requests_mock):
#
#         mocked_response = mock.Mock()
#         requests_mock.post.return_value = mocked_response
#         mocked_response.status_code = 204
#
#         send_data('url', 'measurement', {'tag': 'value'}, 2, 1490223248024070912)
#
#         self.assertEquals(1, requests_mock.post.call_count)
#
#         requests_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912', timeout=30)
#
#     @mock.patch('grafana_celery_client.influx.requests')
#     def test_tags_string(self, requests_mock):
#
#         mocked_response = mock.Mock()
#         requests_mock.post.return_value = mocked_response
#         mocked_response.status_code = 204
#
#         send_data('url', 'measurement', 'tag=value', 2, 1490223248024070912)
#
#         self.assertEquals(1, requests_mock.post.call_count)
#         requests_mock.post.assert_called_with('url', data='measurement,tag=value value=2 1490223248024070912', timeout=30)
#
#     @mock.patch('grafana_celery_client.influx.requests')
#     def test_bad_request_500(self, requests_mock):
#
#         mocked_response = mock.Mock()
#         requests_mock.post.return_value = mocked_response
#         mocked_response.status_code = 500
#         mocked_response.text = 'Error'
#
#         self.assertRaises(BadRequest, send_data, 'url', 'measurement', 'tag=value', 2, 1490223248024070912)
#
#     @mock.patch('grafana_celery_client.influx.requests')
#     def test_bad_request_400(self, requests_mock):
#
#         mocked_response = mock.Mock()
#         requests_mock.post.return_value = mocked_response
#         mocked_response.status_code = 400
#         mocked_response.text = 'Error'
#
#         self.assertRaises(BadRequest, send_data, 'url', 'measurement', 'tag=value', 2, 1490223248024070912)
#
#
#
