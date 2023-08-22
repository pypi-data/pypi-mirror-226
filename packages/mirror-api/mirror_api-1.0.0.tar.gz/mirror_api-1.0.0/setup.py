# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirror_api']

package_data = \
{'': ['*']}

install_requires = \
['fastapi', 'python-multipart', 'typer', 'uvicorn[standard]']

setup_kwargs = {
    'name': 'mirror-api',
    'version': '1.0.0',
    'description': 'An API that returns the structure of the request as the response',
    'long_description': '\n\n[![](https://codecov.io/gh/nickderobertis/mirror-api/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/mirror-api)\n[![PyPI](https://img.shields.io/pypi/v/mirror-api)](https://pypi.org/project/mirror-api/)\n![PyPI - License](https://img.shields.io/pypi/l/mirror-api)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/mirror-api/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/mirror-api/)\n\n\n#  mirror-api\n\n## Overview\n\nAn API that returns the structure of the request as the response\n\n## Getting Started\n\nInstall `mirror-api`:\n\n```\npip install mirror-api\n```\n\nA simple example:\n\n```python\nimport mirror_api\n\n# Do something with mirror_api\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/mirror-api/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/mirror-api/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](\nhttps://github.com/nickderobertis/mirror-api/blob/main/DEVELOPING.md\n) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n',
    'author': 'Nick DeRobertis',
    'author_email': 'derobertis.nick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
