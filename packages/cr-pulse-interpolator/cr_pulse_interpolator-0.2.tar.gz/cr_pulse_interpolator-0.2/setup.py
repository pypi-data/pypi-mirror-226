#!/usr/bin/env python3

from setuptools import setup

setup(name='cr_pulse_interpolator', 
      version='0.2',
      description='Full electric-field waveform interpolation for air shower simulations', 
      url='https://github.com/nu-radio/cr-pulse-interpolator',
      author='Arthur Corstanje',
      author_email='a.corstanje@astro.ru.nl', 
      license='GNU General Public License v3.0',
      install_requires=['numpy', 'scipy', 'matplotlib', 'h5py'],
      packages= ['cr_pulse_interpolator'], 
      zip_safe=False)
