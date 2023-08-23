# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrop']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.10.0.0']

setup_kwargs = {
    'name': 'pyrop',
    'version': '1.0.0',
    'description': 'Imperative-style railway-oriented programming in Python',
    'long_description': '\n\n[![](https://codecov.io/gh/nickderobertis/pyrop/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/pyrop)\n[![PyPI](https://img.shields.io/pypi/v/pyrop)](https://pypi.org/project/pyrop/)\n![PyPI - License](https://img.shields.io/pypi/l/pyrop)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/pyrop/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.9%20%7C%203.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.9%20%7C%203.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.9%20%7C%203.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/pyrop/)\n\n\n#  pyrop\n\n## Overview\n\nImperative-style railway-oriented programming in Python\n\n## Getting Started\n\nInstall `pyrop`:\n\n```\npip install pyrop\n```\n\nA simple example:\n\n```python\nimport pyrop\n\n# Do something with pyrop\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/pyrop/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/pyrop/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](\nhttps://github.com/nickderobertis/pyrop/blob/main/DEVELOPING.md\n) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n',
    'author': 'Nick DeRobertis',
    'author_email': 'derobertis.nick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
