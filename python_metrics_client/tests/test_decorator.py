from math import isclose

from unittest import mock
import time
from datetime import datetime

from python_metrics_client.tests.base import TestCase
from python_metrics_client.duration import timeit


@timeit(environment='dev')
def decorated_function():
    time.sleep(0.2)

ellapsed_time_position = 2
timestamp_position = 4

def parse_timestamp(text_ts):
    ts = datetime.strptime(text_ts.rsplit(".", 1)[0], "%Y-%m-%dT%H:%M:%S")
    return ts.timestamp()


class DecoratorTest(TestCase):

    @mock.patch('python_metrics_client.duration._send_metric.delay')
    def test_timeit(self, requests_mock):
            decorated_function()
            args = requests_mock.call_args
            self.assertEqual(len(args), 2)
            args = args[0]
            expected_args =  ('dev', 'duration', 0.2, [{'process_name': 'decorated_function'}], '2017-10-25T10:00:00', None, None)
            for step, (arg, expected_arg) in enumerate(zip(args, expected_args)):
                if step == ellapsed_time_position:
                    assert isclose(arg, expected_arg, abs_tol=0.001)
                elif step == timestamp_position:
                    assert isclose(parse_timestamp(arg), datetime.utcnow().timestamp(), abs_tol=0.5)
                else:
                    self.assertEqual(arg, expected_arg)
