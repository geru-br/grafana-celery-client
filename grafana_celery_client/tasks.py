

# from grafana_celery_client.influx import send_data as actual_send_data


def send_data(self, dimension, value, extra_data=None, timestamp=None):

    actual_send_data(self.app.conf.grafana_celery_client_url, dimension, value, extra_data=extra_data, timestamp=timestamp)
