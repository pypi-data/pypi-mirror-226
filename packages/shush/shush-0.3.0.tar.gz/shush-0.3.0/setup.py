# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shush']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shush',
    'version': '0.3.0',
    'description': 'Subprocesses for humans.',
    'long_description': None,
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
