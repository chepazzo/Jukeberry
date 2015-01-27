#!/usr/bin/env python

import sys
## Without this, Flask complains that the .egg file
## is not a directory.
#sys.argv.append('--old-and-unmanageable')

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
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    data_files=[
        ('/etc', ['config/jukeberry.conf']),
        ('/etc/init.d/', ['install/deb/jukeberry']),
        ('/etc/init/', ['install/deb/jukeberry.conf']),
    ],
    entry_points={
        'console_scripts': {
            'start_jukeberry = jukeberry.server:main',
            'juke-loadcatalog = jukeberry.server:load_catalog'
        }
    },
)
