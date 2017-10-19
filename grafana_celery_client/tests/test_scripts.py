# -*- coding: utf-8 -*-
import mock
from click.testing import CliRunner
from base import TestCase
from grafana_celery_client.scripts.grafana import influx_send_data, tasks_send_data


class ScriptsTest(TestCase):

    @mock.patch('grafana_celery_client.tasks.send_data')
    def test_tasks_send_data(self, send_data_mock):

        runner = CliRunner()

        response = runner.invoke(tasks_send_data, ['measurement', 'tag=value', '2', '-t 1490223248024070912'])

        self.assertEquals(response.exit_code, 0)

        self.assertEquals(1, send_data_mock.delay.call_count)
        send_data_mock.delay.assert_called_with(u'measurement', u'tag=value', u'2')
