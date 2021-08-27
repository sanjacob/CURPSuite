#!/usr/bin/env python3
from setuptools import setup
from curp.__about__ import (__title__, __version__, __summary__, __uri__, __author__, __email__, __license__)

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    url=__uri__,
    author=__author__,
    author_email=__email__,
    license=__license__)
