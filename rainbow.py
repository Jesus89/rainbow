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


@Singleton
class Rainbow(object):

    def __init__(self):
        self.functions = {}

    def json_str(self, data):
        return json.dumps(json.loads(data))

    def register(self, key, function):
        self.functions[key] = function

    def call(self, key, args=None, kwargs=None):
        if args is None:
            args = {}
        else:
            args = json.loads(args)
        if kwargs is None:
            kwargs = {}
        else:
            kwargs = json.loads(kwargs)
        ret = {}
        ret['result'] = self.functions[key](*args, **kwargs)
        return json.dumps(ret)


app = Rainbow()


# Public methods
def register(key):
    def decorator(function):
        app.register(key, function)
        return function
    return decorator
