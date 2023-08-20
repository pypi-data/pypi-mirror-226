#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noun-splitter",
    version="0.0.1",
    author="Mathias Haugestad",
    author_email="mhaugestad@gmail.com",
    description="Python module to decompose nouns based on the SECOS algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhaugestad/noun-splitter",
    packages=setuptools.find_packages(include=['secos', 'secos.*']),
    install_requires=['scipy', 'numpy', 'pytest', 'importlib-resources', 'requests', 'tqdm'],
    python_requires='>=3.6',
    download_url='https://github.com/mhaugestad/noun-splitter/archive/refs/tags/0.0.1.tar.gz'
)