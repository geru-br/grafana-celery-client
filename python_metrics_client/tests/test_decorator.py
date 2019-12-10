
import mock
import time
from freezegun import freeze_time
from datetime import datetime
from python_metrics_client.tests.base import TestCase
from python_metrics_client.duration import timeit


@timeit(environment='dev')
def decorated_function():
    time.sleep(1)


class DecoratorTest(TestCase):

    @mock.patch('python_metrics_client.duration._send_metric.delay')
    def test_timeit(self, requests_mock):
        with freeze_time(datetime(2017, 10, 25, 10, 00, 00)):
            with mock.patch('python_metrics_client.duration.timer') as mocked_timer:
                mocked_timer.return_value = 0.0
                decorated_function()
                # With freezegun, default_timer() wll always get the same time, so time elapsed will be 0.0.
                # Time elapsed is unpredictable otherwise
                requests_mock.assert_called_with('dev', 'duration', 0.0, [{'process_name': 'decorated_function'}],
                                             '2017-10-25T10:00:00', None, None)
