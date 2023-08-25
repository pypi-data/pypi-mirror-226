#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# ccpayment - api
# https://github.com/cctip/ccpayment-sdk-python/ccpayment

from setuptools import setup, find_packages
# from codecs import open
import io
from os import path

# --- get version ---
version = "unknown"
with open("ccpayment/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')
# --- /get version ---


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ccpayment',
    version=version,
    description='ccpayment API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cctip/ccpayment-sdk-python/ccpayment',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    platforms=['all'],
    packages=find_packages(exclude=[]),
    install_requires=[],
)

