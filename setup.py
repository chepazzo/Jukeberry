#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import sys

from setuptools import setup, find_packages

# Get version from pkg index
from jukeberry import __version__
from jukeberry import __author__
from jukeberry import __maintainer__
from jukeberry import __url__
from jukeberry import __email__
from jukeberry import __doc__
from jukeberry import __shortdesc__
from jukeberry import __name__ as __packagename__

desc = __shortdesc__
long_desc = __doc__

requires = [
    'Flask>=0.10.1',
    'eyeD3>=0.7.5',
]

setup(name=__packagename__,
    version=__version__,
    description=desc,
    long_description=long_desc,
    author=__author__,
    author_email=__email__,
    url=__url__,
    zip_safe=False,
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    scripts=[
        'bin/juke-loadcatalog',
    ],
    data_files=[
        ('/etc', ['config/jukeberry.ini']),
    ],
    entry_points={
        'console_scripts': {
            'start_jukeberry = jukeberry.runserver:main',
        }
    },
)
