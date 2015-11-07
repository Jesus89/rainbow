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


def Singleton(class_):
    class class_w(class_):
        _instance = None

        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w, class_).__new__(class_, *args, **kwargs)
                class_w._instance.__initialized = False
            return class_w._instance

        def __init__(class_, *args, **kwargs):
            if class_w._instance.__initialized:
                return
            super(class_w, class_).__init__(*args, **kwargs)
            class_w._instance.__initialized = True

    class_w.__name__ = class_.__name__
    return class_w


@Singleton
class Rainbow(object):
    pass

app = Rainbow()
