#!/usr/bin/env python

from distutils.core import setup
import os


setup(name='RoboMachine',
      version='0.1',
      description='Test data generator for Robot Framework',
      author='Mikko Korpela',
      packages=['robomachine'],
      package_dir={'':'src'},
      scripts = [os.path.join('src','bin','robomachine')]
     )
