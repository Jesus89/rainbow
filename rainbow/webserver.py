# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'


def run(host='0.0.0.0'):
    import os
    import gevent.pywsgi
    import paste.urlparser
    http_server = gevent.pywsgi.WSGIServer(
        (host, 8000), paste.urlparser.StaticURLParser(os.path.dirname(__file__)))
    http_server.start()
