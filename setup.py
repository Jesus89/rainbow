#!/usr/bin/env python

from setuptools import setup

import rainbow

setup(name='pyrainbow',
      version=rainbow.__version__,
      description=rainbow.__doc__,
      author=rainbow.__author__,
      author_email=rainbow.__email__,
      url='https://github.com/bqlabs/rainbow',
      download_url='https://pypi.python.org/pypi/pyrainbow',
      license=rainbow.__license__,
      py_modules=['rainbow'],
      install_requires=['paste>=2.0.2',
                        'gevent>=1.0.2',
                        'gevent-zeromq>=0.2.5',
                        'gevent-websocket>=0.9.5'],
      extras_require=dict(develop=['nose>=1.3.1']),
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7']
      )
