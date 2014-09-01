#!/usr/bin/env python
"""
sentry-turbosms
===============

A Sentry extension which integrates TurboSMS.

:copyright: (c) 2014 by Denis Gonsiorovsky.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry',
    'mysql-connector-python>=1.2.2'
]

setup(
    name='sentry-turbosms',
    version='0.0.1',
    author='Denis Gonsiorovsky',
    author_email='dns.gnsr@gmail.com',
    url='https://github.com/gonsiorovsky/sentry-turbosms',
    description='A Sentry extension which integrates TurboSMS.',
    long_description=__doc__,
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'turbosms = sentry_turbosms',
        ],
       'sentry.plugins': [
            'turbosms = sentry_turbosms.plugin:TurboSMSPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
