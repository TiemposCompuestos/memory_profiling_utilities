#!/usr/bin/env python

import os
import sys

from distutils.core import setup

name = "memory_profiling_utilities"

rootdir = os.path.abspath(os.path.dirname(__file__))

# Restructured text project description read from file
long_description = open(os.path.join(rootdir, 'README.md')).read()

# Build a list of all project modules
packages = []
for dirname, dirnames, filenames in os.walk(name):
    if '__init__.py' in filenames:
        packages.append(dirname.replace('/', '.'))

package_dir = {name: name}

setup(
    name = name,
    description = 'a couple tools for memory profiling',
    long_description = long_description,
    url = 'https://github.com/TiemposCompuestos/memory_profiling_utilities',
    author = 'Federico Alvarez',
    author_email = 'federicoalvarez.puan@gmail.com',
    packages = packages,
    package_dir = package_dir,
    install_requires = [
        'memory_profiler'
    ]
)
    