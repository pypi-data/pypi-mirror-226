# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deskaone_requests',
 'deskaone_requests.Client',
 'deskaone_requests.Exceptions',
 'deskaone_requests.Firebase',
 'deskaone_requests.Requests',
 'deskaone_requests.Utils']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'bs4>=0.0.1,<0.0.2',
 'colorama>=0.4.5,<0.5.0',
 'fastapi[all]>=0.101.1,<0.102.0',
 'flask>=2.2.3,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'html5lib>=1.1,<2.0',
 'install-jdk>=0.3.0,<0.4.0',
 'polling2>=0.5.0,<0.6.0',
 'polling>=0.3.2,<0.4.0',
 'pycryptodome>=3.6.4',
 'pyrebase4>=4.7.1,<5.0.0',
 'pysocks>=1.7.1,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests[socks]>=2.11.1,<3.0.0',
 'sqlalchemy==1.4.29']

setup_kwargs = {
    'name': 'deskaone-requests',
    'version': '0.0.1rc10',
    'description': '',
    'long_description': 'pip install deskaone-requests',
    'author': 'DesKaOne',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
