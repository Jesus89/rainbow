# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project
"""
Rainbow is a micro-framework for Python RPC+P&S communication over WebSockets.
"""

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'

__version__ = '0.0.0'


def Singleton(cls):
    class cls_w(cls):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls_w._instance is None:
                cls_w._instance = super(cls_w, cls).__new__(cls, *args, **kwargs)
                cls_w._instance.__initialized = False
            return cls_w._instance

        def __init__(cls, *args, **kwargs):
            if cls_w._instance.__initialized:
                return
            super(cls_w, cls).__init__(*args, **kwargs)
            cls_w._instance.__initialized = True

    cls_w.__name__ = cls.__name__
    return cls_w


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
        Process request according to JSON-RPC 2.0 Specs <http://www.jsonrpc.org/specification>
        Input and output data types are JSON string
        """
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
        if 'params' in request and isinstance(request['params'], list):
            args = request['params']
        else:
            args = {}
        if 'params' in request and isinstance(request['params'], dict):
            kwargs = request['params']
        else:
            kwargs = {}
        result = self.call(request['method'], args, kwargs)
        return result

    def call(self, key, args={}, kwargs={}):
        if isinstance(key, unicode):
            if key in self.functions:
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


# Public methods
def register(key):
    def decorator(function):
        dealer.register(key, function)
        return function
    return decorator
