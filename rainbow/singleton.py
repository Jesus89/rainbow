# -*- coding: utf-8 -*-
# This file is part of the Rainbow Project

__author__ = 'Jesús Arroyo Torrens'
__email__ = 'jesus.arroyo@bq.com'
__copyright__ = 'Copyright (c) 2015 Mundo Reader S.L.'
__license__ = 'GPLv2'


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
