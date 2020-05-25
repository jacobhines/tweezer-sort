# -*- coding: utf-8 -*-
"""
Created on Sun May 24 08:53:19 2020

@author: Jacob
"""

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tweezerlyze',
    version='0.1.0',
    description='Measures, interprets, and sorts atoms held in an array of optical tweezers.',
    long_description=readme,
    author='Jacob Hines',
    author_email='hines@stanford.edu',
    url='https://github.com/jacobhines/tweezer_sort',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)