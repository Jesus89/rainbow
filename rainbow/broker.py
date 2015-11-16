# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'

import json
import gevent
import datetime
from gevent_zeromq import zmq
from geventwebsocket.handler import WebSocketHandler

from rainbow.singleton import Singleton


@Singleton
class Broker(object):
    """
    It is responsible for sending the event information
    to the subscribers when a topic is published
    """
    def run(self, host='0.0.0.0'):
        context = zmq.Context()
        gevent.spawn(zmq_server, context)
        gevent.pywsgi.WSGIServer((host, 8081), BrokerWebSocket(context),
                                 handler_class=WebSocketHandler).start()
        # Event socket
        self.socket = context.socket(zmq.PUB)
        self.socket.connect('tcp://' + host + ':5000')

    def publish(self, event=None, data=None):
        topic = {'time': datetime.datetime.now().isoformat(),
                 'event': event,
                 'data': data}
        self.socket.send(json.dumps(topic))


def zmq_server(context):
    """
    Funnel messages coming from the external tcp socket to an inproc socket
    """
    sock_incoming = context.socket(zmq.SUB)
    sock_outgoing = context.socket(zmq.PUB)
    sock_incoming.bind('tcp://*:5000')
    sock_outgoing.bind('inproc://queue')
    sock_incoming.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        msg = sock_incoming.recv()
        sock_outgoing.send(msg)


class BrokerWebSocket(object):
    """
    Funnel messages coming from an inproc zmq socket to the websocket
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, environ, start_response):
        ws = environ['wsgi.websocket']
        sock = self.context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect('inproc://queue')
        while True:
            msg = sock.recv()
            ws.send(msg)
