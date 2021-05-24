#!/usr/bin/env python

from setuptools import setup, find_packages, Extension
import numpy as np


setup(name='cloudy',
      version='0.1',
      description='Python Tools for running cloudy models',
      url='https://github.com/vikramkhaire/cloudy',
      include_dirs=np.get_include(),
      install_requires=['astropy',
                        'numpy',
                        'matplotlib'],
     )
