#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

base_path = os.path.dirname(__file__)


with open(os.path.join(base_path, "README.md")) as f:
    long_description = f.read()

with open(os.path.join(base_path, "socks_client/__version__.py")) as f:
    try:
        VERSION = re.findall(r"^__version__ = '([^']+)'\r?$", f.read(), re.M)[0]
    except:
        VERSION = None


setup(
    name="socks-client",
    version=VERSION,
    description="Supports both TCP and UDP client with the implementation of SOCKS5 and SOCKS4 protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Plattanus",
    author_email="plattanus@outlook.com",
    url="https://github.com/plattanus/socks-client.git",
    license="MIT License",
    keywords=["socks", "socks5", "socks4", "proxy", "asyncio"],
    install_requires=[],
    python_requires=">=3.7",
    packages=[
        "socks_client",
    ],
)
