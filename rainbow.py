# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project
"""
Rainbow is a micro-framework for Python RPC+P&S communication over WebSockets.
"""

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'

__version__ = '0.0.3'


def Singleton(cls):
    class cls_w(cls):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls_w._instance is None:
                cls_w._instance = super(cls_w, cls).__new__(cls, *args, **kwargs)
                cls_w._instance.__initialized = False
            return cls_w._instance

        def __init__(cls, *args, **kwargs):
            if not cls_w._instance.__initialized:
                super(cls_w, cls).__init__(*args, **kwargs)
                cls_w._instance.__initialized = True

    cls_w.__name__ = cls.__name__
    return cls_w


################################################################################
# Dealer: is responsible for routing a call originating from the Caller to the #
#         Callee and route back results or errors                              #
################################################################################


class JSONRPCException(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data


class ParseError(JSONRPCException):
    def __init__(self):
        JSONRPCException.__init__(self, -32700, 'Parse error')


class InvalidRequest(JSONRPCException):
    def __init__(self):
        JSONRPCException.__init__(self, -32600, 'Invalid Request')


class MethodNotFound(JSONRPCException):
    def __init__(self):
        JSONRPCException.__init__(self, -32601, 'Method not found')


class InvalidParams(JSONRPCException):
    def __init__(self):
        JSONRPCException.__init__(self, -32602, 'Invalid params')


class InternalError(JSONRPCException):
    def __init__(self, data):
        JSONRPCException.__init__(self, -32603, 'Internal error', data)


import json


@Singleton
class Dealer(object):

    def __init__(self):
        self.functions = {}

    def register(self, key, function):
        """
        Register function in dictionary with the provided key
        """
        self.functions[key] = function

    def process_request(self, request):
        """
        Process request according to JSON-RPC 2.0 Specs:
            <http://www.jsonrpc.org/specification>
        Input and output data types are JSON string
        """
        response = None
        try:
            request = json.loads(request)
        except:
            # Parse error
            response = {'jsonrpc': '2.0',
                        'error': {'code': ParseError().code,
                                  'message': ParseError().message},
                        'id': None}
        else:
            if isinstance(request, list):
                if not request:
                    # Empty array
                    response = {'jsonrpc': '2.0',
                                'error': {'code': InvalidRequest().code,
                                          'message': InvalidRequest().message},
                                'id': None}
                else:
                    # Batch call
                    response = []
                    for req in request:
                        res = self._single_request(req)
                        if res is not None:
                            # Not notification
                            response += [res]
                    if not response:
                        # All notifications
                        response = None
            else:
                # Single call
                response = self._single_request(request)
        finally:
            if response is not None:
                return json.dumps(response)

    def _single_request(self, request):
        response = None
        try:
            self._verify_request(request)
            result = self._execute_request(request)
        except JSONRPCException as e:
            response = {'jsonrpc': '2.0',
                        'error': {'code': e.code, 'message': e.message},
                        'id': None}
            if isinstance(e, InternalError):
                response['error']['data'] = e.data
            if isinstance(e, MethodNotFound) or isinstance(e, InvalidParams):
                response['id'] = request['id']
        else:
            if 'id' in request:
                response = {'jsonrpc': '2.0',
                            'result': result,
                            'id': request['id']}
            else:
                # Notification
                response = None
        finally:
            return response

    def _verify_request(self, request):
        if not isinstance(request, dict) or \
           'jsonrpc' not in request or \
           request['jsonrpc'] != '2.0':
            raise InvalidRequest

    def _execute_request(self, request):
        args = {}
        kwargs = {}
        result = None
        if 'params' in request and isinstance(request['params'], list):
            args = request['params']
        if 'params' in request and isinstance(request['params'], dict):
            kwargs = request['params']
        result = self.call(request['method'], args, kwargs)
        return result

    def call(self, key, args={}, kwargs={}):
        result = None
        if isinstance(key, unicode):
            if key == '_functions':
                return self.functions.keys()
            elif key in self.functions:
                try:
                    result = self.functions[key](*args, **kwargs)
                except TypeError as e:
                    raise InvalidParams
                except Exception as e:
                    raise InternalError(e.message)
                else:
                    return result
            else:
                raise MethodNotFound
        else:
            raise InvalidRequest


dealer = Dealer()

try:
    from geventwebsocket import WebSocketApplication

    class DealerApplication(WebSocketApplication):
        def on_message(self, message):
            response = dealer.process_request(message)
            if response is not None:
                self.ws.send(response)
except:
    pass


################################################################################
# Broker: is responsible for sending the event information to the subscribers  #
#         when a topic is published                                            #
################################################################################


try:
    import gevent
    import datetime
    from gevent_zeromq import zmq
    from geventwebsocket.handler import WebSocketHandler

    @Singleton
    class Broker(object):
        def __init__(self, host='0.0.0.0'):
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
except:
    pass


################################################################################
# Public methods: register, publish, run                                       #
################################################################################


def register(key):
    def decorator(function):
        dealer.register(key, function)
        return function
    return decorator


def publish(event=None, data=None):
    global broker
    broker.publish(event, data)


def run(host='0.0.0.0', webserver=False, webbrowser=False, debug=False):
    print 'Running server {0}'.format(host)

    if webserver:
        import os
        import paste.urlparser
        http_server = gevent.pywsgi.WSGIServer(
            (host, 8000),
            paste.urlparser.StaticURLParser(os.path.dirname('test/')))
        http_server.start()
        if webbrowser:
            import webbrowser
            webbrowser.open('http://' + host + ':8000/client.html')

    try:
        global broker
        broker = Broker(host)
        from collections import OrderedDict
        from geventwebsocket import WebSocketServer, Resource
        dealer_server = WebSocketServer((host, 8080),
                                        Resource(OrderedDict({'/': DealerApplication})),
                                        debug=debug)
        dealer_server.serve_forever()
    except KeyboardInterrupt:
        dealer_server.close()
    except Exception:
        pass


if __name__ == '__main__':  # pragma: no cover

    # Register function
    @register('add')
    def add(a, b):
        publish('event.add', '{0} + {1}'.format(a, b))
        return a + b

    @register('sub')
    def sub(a, b):
        publish('event.sub', '{0} - {1}'.format(a, b))
        return a - b

    # Start server
    run(host='0.0.0.0', webserver=True, webbrowser=True)
