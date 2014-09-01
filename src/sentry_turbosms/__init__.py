"""
sentry_turbosms
~~~~~~~~~~~~~~~

:copyright: (c) 2014 by Denis Gonsiorovsky.
:license: BSD, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-turbosms').version
except Exception, e:
    VERSION = 'unknown'
