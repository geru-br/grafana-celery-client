import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION.txt')) as f:
    VERSION = f.read().strip('\r\n')

requires = [r.strip('\r\n')
            for r in open('requirements.txt').readlines()]

entry_points = None
if os.environ.get('STANDALONE'):
    entry_points = """\
      [console_scripts]
      manage = grafana_celery_client.manage:cli
      """


setup(name='grafana_celery_client',
      version=VERSION,
      description='grafana celery client',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='',
      author_email='',
      url='',
      keywords='grafana',
      packages=find_packages(exclude=[
          'grafana_celery_client.test', 'grafana_celery_client.test.*']),
      include_package_data=True,
      zip_safe=False,
      test_suite='grafana_celery_client',
      install_requires=requires,
      entry_points=entry_points,
      )
