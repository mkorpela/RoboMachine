#!/usr/bin/env python

from distutils.core import setup
import os
from setuptools import find_packages


setup(name='RoboMachine',
      version='0.1',
      description='Test data generator for Robot Framework',
      author='Mikko Korpela',
      packages=find_packages(),
      scripts = [os.path.join('bin','robomachine'),
                 os.path.join('bin','robomachine.bat')],
      install_requires = ['pyparsing']
     )
