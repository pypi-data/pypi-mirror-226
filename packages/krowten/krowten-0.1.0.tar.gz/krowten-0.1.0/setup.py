# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['krowten', 'krowten.models', 'krowten.renderer']

package_data = \
{'': ['*']}

install_requires = \
['quart>=0.18.4,<0.19.0']

setup_kwargs = {
    'name': 'krowten',
    'version': '0.1.0',
    'description': 'A library for graphs and taking actions on them.',
    'long_description': 'A graph creation library **Under Development**',
    'author': 'utsavan',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
