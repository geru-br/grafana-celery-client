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
      manage = python_metrics_client.manage:cli
      """


setup(name='python_metrics_client',
      version=VERSION,
      description='python metrics client',
      classifiers=[
          "Programming Language :: Python",
      ],
      author='',
      author_email='',
      url='',
      keywords='grafana',
      packages=find_packages(exclude=[
          'python_metrics_client.test', 'python_metrics_client.test.*']),
      include_package_data=True,
      zip_safe=False,
      test_suite='python_metrics_client',
      install_requires=requires,
      entry_points=entry_points,
      )
