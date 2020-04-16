import os

from setuptools import setup, find_packages

requires = [
    'requests>=2.3.0',
    'influxdb==4.1.1',
]

entry_points = None
if os.environ.get('STANDALONE'):
    entry_points = """\
      [console_scripts]
      manage = python_metrics_client.manage:cli
      """


setup(
    name='python_metrics_client',
    version='0.11.4',
    description='python metrics client',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='',
    author_email='',
    url='',
    keywords='grafana,influxdb,metrics,pyramid,celery',
    packages=find_packages(exclude=[
        'python_metrics_client.test',
        'python_metrics_client.test.*'
    ]),
    include_package_data=True,
    zip_safe=False,
    test_suite='python_metrics_client',
    install_requires=requires,
    entry_points=entry_points,
  )
