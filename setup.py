import os

from setuptools import setup, find_packages

requires = [
    'requests>=2.3.0',
    'celery==4.0.2',
    'click==6.7',
    'influxdb==5.2.3',
]

extras_require = {
    'tests': [
        'coverage==4.4.1',
        'freezegun==0.3.12',
        'mock==2.0.0',
        'nose==1.3.7',
        'tox==3.14.6',
    ],
}

dev_ = ['ipdb==0.8', 'ipython==5.1.0']

extras_require['dev'] = extras_require['tests'] + dev_

entry_points = None
if os.environ.get('STANDALONE'):
    entry_points = """\
      [console_scripts]
      manage = python_metrics_client.manage:cli
      """


setup(
    name='python_metrics_client',
    version='0.11.5',
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
    extras_require=extras_require,
    entry_points=entry_points,
  )
