# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project
"""
Rainbow is a micro-framework for Python RPC+Pub/Sub communication over WebSockets.
"""

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'

__version__ = '0.0.7'

try:
    from rainbow.dealer import Dealer
    from rainbow.broker import Broker

    dealer = Dealer()
    broker = Broker()
except:
    pass


def register(function):
    dealer.register(function)
    return function


def publish(event=None, data=None):
    broker.publish(event, data)


def run(host='0.0.0.0', avahi=False, webserver=False, webbrowser=False, debug=False):
    print('Running server ' + host)
    avahi_server = None
    if avahi:
        from rainbow import avahi
        avahi_server = avahi.run()
    if webserver:
        from rainbow import webserver
        webserver.run(host)
        if webbrowser:
            import webbrowser
            webbrowser.open('http://' + host + ':8000')
    try:
        broker.run(host)
        dealer.run_forever(host, debug)
    except:
        if avahi_server:
            avahi_server.kill()
