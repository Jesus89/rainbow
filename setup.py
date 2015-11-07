#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import rainbow

setup(name='Rainbow',
      version=rainbow.__version__,
      description=rainbow.__doc__,
      long_description=open('README.md').read(),
      author=rainbow.__author__,
      author_email=rainbow.__email__,
      url='https://github.com/bqlabs/rainbow',
      license=rainbow.__license__,
      py_modules=['rainbow'],
      extra_requires=['nose>=1.3.1']
      )
