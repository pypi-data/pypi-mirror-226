# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'macrometa_source_mysql'}

packages = \
['macrometa_source_mysql',
 'macrometa_source_mysql.sync_strategies',
 'sync_strategies']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.1.0',
 'c8connector>=0.0.32',
 'mysql-replication==0.43',
 'pendulum==2.1.2',
 'pipelinewise-singer-python==1.2.0',
 'plpygis==0.2.1',
 'prometheus-client==0.16.0',
 'tzlocal==2.1']

entry_points = \
{'console_scripts': ['macrometa-source-mysql = macrometa_source_mysql:main']}

setup_kwargs = {
    'name': 'macrometa-source-mysql',
    'version': '0.0.14',
    'description': 'Macrometa Source for extracting data from MySQL database.',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
