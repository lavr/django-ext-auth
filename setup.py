#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import codecs
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

from setuptools import Command, setup


def find_version(*file_paths):
    version_file_path = os.path.join(os.path.dirname(__file__),
                                     *file_paths)
    version_file = codecs.open(version_file_path,
                               encoding='utf-8').read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


settings.update(
    name='django_ext_auth',
    version=find_version('django_ext_auth/__init__.py'),
    description='Quick and dirty external session validation',
    long_description=__doc__,
    author='Sergey Lavrinenko',
    author_email='s@lavr.me',
    url='https://github.com/lavr/django-ext-auth',
    packages=['django_ext_auth',
              'django_ext_auth.backend',
              ],
    install_requires=['requests', ],
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ),
)

setup(**settings)
