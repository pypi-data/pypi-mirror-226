#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

setup(name='cr_pulse_interpolator', 
      version='0.1',
      description='Full electric-field waveform interpolation for air shower simulations', 
      url='https://github.com/nu-radio/cr-pulse-interpolator',
      author='Arthur Corstanje',
      author_email='a.corstanje@astro.ru.nl', 
      license='GNU General Public License v3.0',
      install_requires=['numpy', 'scipy', 'matplotlib', 'h5py'],
      packages=find_packages(), 
      zip_safe=False)
