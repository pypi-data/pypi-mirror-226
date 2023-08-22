# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['learning_poetry']

package_data = \
{'': ['*']}

install_requires = \
['idna>=3.4,<4.0']

setup_kwargs = {
    'name': 'learning-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pető Tamás',
    'author_email': 'petotamas0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
