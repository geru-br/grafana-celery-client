# Python metics client

This lib should be used by pyramid. It can be used standalone. :-)

## Dependences
```
pyramid
celery
```

## Integration with Pyramid

### Instalation

Add to project requirements.txt

```shell
...
-e git+https://github.com/geru-br/python-metrics-client@master8#egg=python_metrics_client
...

```

### Configuration
Add to project __init__.py or main() method

```python
	
    ...
    settings['python_metrics_client.url'] = get_from_env_or_settings(
        'python_metrics_client.url', settings,
        default='http://52.91.126.40:8086/write?db=graphite'
    )
    ...
    config.include('python_metrics_client')
    ...

```

### Use

```

import time
from python_metrics_client.tasks import send_data

# Timestamp must be sent in microseconds
send_data.delay(
    'ccb.pool.size',
    'environment={},system=core'.format('dev'),
    count, timestamp=time.time() * 1000000000
)
```

## Multiple metric engine functions

A new set of functions were added to support multiple types of metrics. By default, it uses InfluxDB, but graphite is also supported. 

### Interoperability

InfluxDb and grapite are different in the way they organize metrics. Graphite metrics are stored in a tree structured with levels separated by dots. Influx uses a more complex strucutre allowing the use of tags. To ensure full compatibility, tags are passed in an optional parameter to the base send_metric function in the form

```
tags = [{'key1': value1},{'key2': value2},...,{'keyN': valueN}]
```

If the metric engine is graphite, the resulting metric path will be

```
'envrionment.value1.value2 ... valueN.metric'

```

If the metrics engin is influxdb, tags will be added to the tags key o the required json strucutre

```
data = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "environment": "dev",
            "key1": "value1",
            "key2": "value2",
            ...
            "keyN": "valueN"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]
```

Environment is a mandatory parameter and treated internaly as a tag

### Usage example
The settings file should contain the appropriate configuration. An example with the default settings is shown below.

```
metrics_server = influxdb.tick.prod.geroo.com.br
metrics_client_protocol = http
metrics_client_port = 80
metrics_client_timeout = 30
metrics_client_type = influxdb
metrics_user = root
metrics_password = root
metrics_environment = prduction

```

Functions should be called as celery tasks althoug it is possible to call functions directly.

```
from datetime import datetime
from python_metrics_client.tasks import send_metric

# Timestamp must be datetime. If it is note provided, utcnow will be used as default
timestamp = datetime.utcnow()

tags = [{'product': 'consignado'}]

send_metric.delay( 'localhost',
                   8086, 
                   approved', 
                   1, 
                   tags=tags, 
                   timestamp=timestamp,
                   environment='production')
```

### Timeit decorator

This library can also be used to measure how long a particular function is taking to run by using the @timeit decorator. The same set of arguments that is supported by send_metric() is supported by @timeit, including server, port, tags and timestamp. A typical usage is shown below.

```
from python_metrics_client.duration import timeit

...


@timeit(environment='production', process_name='loan_rate', tags=[{'service': 'core'}])
def loan_rate(loan):


```

The metric itself can be renamed in the __metric__ argument. If no metric name is provided, it will be set to 'duration' byt default. Tags are optional but useful for metric data grouping measurements from different functions.



## Standalone (using virtualenvwrapper)


```shell
git clone git@github.com:geru-br/python-metrics-client.git
cd python-metrics-client
mkvirtualenv python-metrics-client
pip install -r requirements_standalone.txt
```


## Tests after cloned


```shell
pip install -r requirements_tests.txt
nosetests python_metrics_client/tests

```

