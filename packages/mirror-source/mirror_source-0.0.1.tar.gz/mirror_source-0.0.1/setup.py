# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mirror_source']
install_requires = \
['colorama>=0.4.6,<0.5.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'mirror-source',
    'version': '0.0.1',
    'description': '快速设置国内镜像源,方便记不住源地址的小伙子',
    'long_description': None,
    'author': 'hbh112233abc',
    'author_email': 'hbh112233abc@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}


setup(**setup_kwargs)
