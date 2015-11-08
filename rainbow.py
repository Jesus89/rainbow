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


@Singleton
class Rainbow(object):

    def __init__(self):
        self.functions = {}

    def register(self, key):
        def decorator(function):
            self.functions[key] = function
            return function
        return decorator

    def call(self, key, **params):
        ret = {}
        ret['return'] = self.functions[key](**params)
        return ret

app = Rainbow()
