#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "hbh112233abc@163.com"

import os
from pathlib import Path
import platform
from configparser import ConfigParser
from urllib.parse import urlparse

import toml

from mirror_source.log import *

SOURCES = [
    {"name": "清华", "url": "https://pypi.tuna.tsinghua.edu.cn/simple"},
    {"name": "阿里云", "url": "https://mirrors.aliyun.com/pypi/simple/"},
    {"name": "网易", "url": "https://mirrors.163.com/pypi/simple/"},
    {"name": "豆瓣", "url": "https://pypi.douban.com/simple/"},
    {"name": "百度云", "url": "https://mirror.baidu.com/pypi/simple/"},
    {"name": "华为云", "url": "https://mirrors.huaweicloud.com/repository/pypi/simple/"},
    {"name": "腾讯云", "url": "https://mirrors.cloud.tencent.com/pypi/simple/"},
]


def is_windows() -> bool:
    """Check is windows platform

    Returns:
        bool: result of checked
    """
    return platform.system() == "Windows"


def windows_pip_conf() -> Path:
    """Get Windows platform `pip.ini` file path

    Returns:
        Path: the path of `pip.ini`
    """
    app_data_dir = Path(os.path.expandvars("%APPDATA%"))
    pip_dir = app_data_dir / "pip"
    if not pip_dir.exists():
        pip_dir.mkdir()
    pip_ini = pip_dir / "pip.ini"
    return pip_ini


def unix_pip_conf() -> Path:
    """Get Unix platform `pip.conf` file path

    Returns:
        Path: the path of `pip.conf`
    """
    pip_dir = Path(os.path.expanduser("~/.pip/"))
    if not pip_dir.exists():
        pip_dir.mkdir()
    pip_conf = pip_dir / "pip.conf"
    return pip_conf


def pip_conf_setting(pip_conf: Path, url: str) -> bool:
    """Write source setting to pip config file

    Args:
        pip_conf (Path): the path of pip config file
        url (str): the url of source

    Returns:
        bool: result of setting
    """
    try:
        conf = ConfigParser()
        conf.add_section("global")
        conf.set("global", "index-url", url)
        conf.add_section("install")
        conf.set("install", "trusted-host", domain(url))
        with open(pip_conf, "w", encoding="utf-8") as f:
            conf.write(f)
        return True
    except Exception as e:
        error(str(e))
        return False


def pip_global_setting(url: str) -> bool:
    """pip global setting

    Args:
        url (str): the url of source

    Returns:
        bool: result of setting
    """
    if is_windows():
        pip_conf = windows_pip_conf()
    else:
        pip_conf = unix_pip_conf()
    return pip_conf_setting(pip_conf, url)


def pipenv_setting(url: str) -> bool:
    """pipenv setting,write source url in .pipfile

    Args:
        url (str): the url of source

    Returns:
        bool: result of setting
    """
    pipfile = Path("./Pipfile")
    if not pipfile.exists():
        return True
    conf = toml.load(pipfile)
    conf["source"] = [
        {
            "url": url,
            "verify_ssl": True,
            "name": domain(url),
        }
    ]
    with open(pipfile, "w", encoding="utf-8") as f:
        toml.dump(conf, f)
    return True


def poetry_setting(url: str) -> bool:
    """poetry setting,write source url in pyproject.toml

    Args:
        url (str): the url of source

    Returns:
        bool: result of setting
    """
    pyproject = Path("./pyproject.toml")
    if not pyproject.exists():
        return True
    conf = toml.load(pyproject)
    conf["tool"]["poetry"]["source"] = [
        {
            "name": domain(url),
            "url": url,
            "default": True,
        }
    ]
    with open(pyproject, "w", encoding="utf-8") as f:
        toml.dump(conf, f)
    return True


def domain(url: str) -> str:
    """Get hostname of the given URL

    Args:
        url (str): url

    Returns:
        str: hostname
    """
    return urlparse(url).hostname


def main():
    res = SOURCES
    options = [f"[{x['name']}]({x['url']})" for x in res]
    selected = ask("请选择要设置的镜像源", options, default="0")
    source = res[int(selected)]
    try:
        result = pip_global_setting(source["url"])
        if not result:
            raise Exception("Global config failed")
        result = pipenv_setting(source["url"])
        if not result:
            raise Exception(".pipfile setting failed")
        result = poetry_setting(source["url"])
        if not result:
            raise Exception("pyproject.toml setting failed")

        success(f"Success setting source: {source['url']}")
    except Exception as e:
        error(e)
