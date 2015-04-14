#!/usr/bin/env python

from distutils.core import setup
import os
from setuptools import find_packages
from os.path import dirname, abspath, join

name = 'Mikko Korpela'
# I might be just a little bit too much afraid of those bots..
address = name.lower().replace(' ', '.')+chr(64)+'gmail.com'

# Get version
CURDIR = dirname(abspath(__file__))
execfile(join(CURDIR, 'robomachine', 'version.py'))

setup(name='RoboMachine',
      version=VERSION,
      description='Test data generator for Robot Framework',
      author=name,
      author_email=address,
      url='https://github.com/mkorpela/RoboMachine',
      packages=find_packages(),
      scripts = [os.path.join('scripts','robomachine'),
                 os.path.join('scripts','robomachine.bat')],
      install_requires = ['pyparsing', 'argparse', 'robotframework']
     )
