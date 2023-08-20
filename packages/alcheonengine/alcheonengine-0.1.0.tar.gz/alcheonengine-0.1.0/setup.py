# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alcheonengine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alcheonengine',
    'version': '0.1.0',
    'description': 'ALCHEON Game Engine',
    'long_description': None,
    'author': 'Andrii Murha',
    'author_email': 'flat.assembly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
