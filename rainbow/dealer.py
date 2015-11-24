# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'

import json
import inspect
from collections import OrderedDict
from geventwebsocket import WebSocketApplication, WebSocketServer, Resource

from rainbow.singleton import Singleton


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


@Singleton
class CallManager(object):
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
                response['id'] = request['id']
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
                return self.functions_descriptor()
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

    def functions_descriptor(self):
        functions = []
        for name, function in self.functions.iteritems():
            m = {}
            m['name'] = name
            m['doc'] = function.__doc__
            args = inspect.getargspec(function).args
            nargs = len(args)
            if nargs > 0:
                defaults = inspect.getargspec(function).defaults
                if defaults is None:
                    defaults = []
                else:
                    defaults = list(defaults)
                defaults = [None] * (nargs - len(defaults)) + defaults
                m['args'] = {}
                for i in range(0, nargs):
                    m['args'].update(self.add_arg(args[i], defaults[i]))
            else:
                m['args'] = None
            functions += [m]
        return functions

    def add_arg(self, name, value):
        arg = {}
        _type = self.json_type(value)
        if isinstance(value, list):
            arg[name] = {'type': _type, 'value': {}}
            for key, val in enumerate(value):
                arg[name]['value'].update(self.add_arg(str(key), val))
        elif isinstance(value, dict):
            arg[name] = {'type': _type, 'value': {}}
            for key, val in value.iteritems():
                arg[name]['value'].update(self.add_arg(key, val))
        else:
            arg[name] = {'type': _type,
                         'value': value}
        return arg

    def json_type(self, value):
        if isinstance(value, bool):
            return 'Boolean'
        if isinstance(value, int) or isinstance(value, float):
            return 'Number'
        if isinstance(value, str) or isinstance(value, unicode):
            return 'String'
        if isinstance(value, list) or isinstance(value, dict):
            return 'Object'
        return 'Null'

_call_manager = CallManager()


class DealerApplication(WebSocketApplication):
    def on_message(self, message):
        response = _call_manager.process_request(message)
        if response is not None:
            try:
                self.ws.send(response)
            except:
                pass


@Singleton
class Dealer(object):
    """
    It is responsible for routing a call originating from the Caller
    to the Callee and route back results or errors
    """
    def register(self, function):
        _call_manager.register(function.__name__, function)

    def run_forever(self, host='0.0.0.0', debug=False):
        try:
            dealer_server = WebSocketServer(
                (host, 8080),
                Resource(OrderedDict({'/': DealerApplication})),
                debug=debug)
            dealer_server.serve_forever()
        except KeyboardInterrupt:
            dealer_server.close()
            raise KeyboardInterrupt
