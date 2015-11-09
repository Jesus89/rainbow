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

import json


class ExampleError(Exception):
    def __init__(self):
        super(ExampleError, self).__init__('Example', 1234)


@Singleton
class Rainbow(object):

    def __init__(self):
        self.functions = {}

    def register(self, key, function):
        self.functions[key] = function

    def call(self, key, args={}, kwargs={}):
        return self.functions[key](*args, **kwargs)

    def json_rpc(self, request=None):
        response = {u'jsonrpc': u'2.0'}
        if self._verify_request(request):
            if isinstance(request['params'], list):
                args = request['params']
            else:
                args = {}
            if isinstance(request['params'], dict):
                kwargs = request['params']
            else:
                kwargs = {}
            response[u'result'] = self.call(request['method'], args, kwargs)
            response[u'id'] = request['id']
        return response

    def _verify_request(self, request):
        return True

    def json_str(self, data):
        return json.dumps(json.loads(data))

app = Rainbow()


# Public methods
def register(key):
    def decorator(function):
        app.register(key, function)
        return function
    return decorator
