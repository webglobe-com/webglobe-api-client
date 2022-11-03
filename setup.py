#!/usr/bin/env python

from distutils.core import setup

setup(name='webglobe-api',
    version='0.0.1',
    description='Webglobe API Python implementation',
    author='Jiri Lunacek',
    author_email='jiri.lunacek@webglobe.com',
    packages=['webglobe_api'],
    # py_modules = ['webglobe_api'],
    entry_points = {
            'console_scripts': ['wg-get-cert=webglobe_api.wg_get_cert:get_cert_cli']
    },
    zip_safe=False,
)