# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mirror_source']
install_requires = \
['colorama>=0.4.6,<0.5.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'mirror-source',
    'version': '0.0.3',
    'description': '快速设置国内镜像源,方便记不住源地址的小伙子',
    'long_description': '# 配置镜像源\n\n> 快速设置国内镜像源,方便记不住源地址的小伙子\n\n## 安装\n\n```shell\npip install mirror_source\n```\n\n## 使用\n\n```shell\npython -m mirror_source\n```\n\n```shell\n\n请选择要设置的镜像源\n\n    [0] [清华](https://pypi.tuna.tsinghua.edu.cn/simple)\n\n    [1] [阿里云](https://mirrors.aliyun.com/pypi/simple/)\n\n    [2] [网易](https://mirrors.163.com/pypi/simple/)\n\n    [3] [豆瓣](https://pypi.douban.com/simple/)\n\n    [4] [百度云](https://mirror.baidu.com/pypi/simple/)\n\n    [5] [华为云](https://mirrors.huaweicloud.com/repository/pypi/simple/)\n\n    [6] [腾讯云](https://mirrors.cloud.tencent.com/pypi/simple/)\n\n[Default:0]> 1\n:) Success setting source: https://mirrors.aliyun.com/pypi/simple/\n```\n\n## 功能介绍\n\n- Windows 环境配置`%APPDATA%/pip/pip.ini`\n\n  ```ini\n  [global]\n  index-url = 镜像源URL\n  [install]\n  trusted-host = 镜像源域名\n  ```\n\n- Linux/Mac 环境配置`~/.pip/pip.conf`\n\n  ```ini\n  [global]\n  index-url = 镜像源URL\n  [install]\n  trusted-host = 镜像源域名\n  ```\n\n- pipenv 环境配置`.Pipfile`\n\n  ```toml\n  [[source]]\n  url = "镜像源URL"\n  verify_ssl = true\n  name = "镜像源域名"\n  ```\n\n- poetry 环境配置`pyproject.toml`\n\n  ```toml\n  [[tool.poetry.source]]\n  name = "镜像源域名"\n  url = "镜像源URL"\n  default = true\n  ```\n',
    'author': 'hbh112233abc',
    'author_email': 'hbh112233abc@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hbh112233abc/mirror-source',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.13',
}


setup(**setup_kwargs)
