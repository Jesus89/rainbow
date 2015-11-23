import json
import unittest
from rainbow import register
from rainbow.dealer import _call_manager as dealer


class RainbowTest(unittest.TestCase):

    def setUp(self):
        # Register functions

        @register
        def pi():
            return 3.141592

        @register
        def hello(name):
            return 'Hello, ' + name

        @register
        def sum(a, b):
            return a + b

        @register
        def list(a, b, c, d):
            return [a, b, c, d]

        @register
        def dict(key, value):
            ret = {}
            ret[key] = value
            return ret

    def test_call_pi(self):
        ret = json.loads('3.141592')
        self.assertEqual(dealer.call(u'pi'), ret)

    def test_call_hello(self):
        args = json.loads('["world"]')
        ret = json.loads('"Hello, world"')
        self.assertEqual(dealer.call(u'hello', args=args), ret)

    def test_call_hello_kw(self):
        kwargs = json.loads('{"name":"world"}')
        ret = json.loads('"Hello, world"')
        self.assertEqual(dealer.call(u'hello', kwargs=kwargs), ret)

    def test_call_sum(self):
        kwargs = json.loads('{"a":3,"b":5}')
        ret = json.loads('8')
        self.assertEqual(dealer.call(u'sum', kwargs=kwargs), ret)

    def test_call_sum_kw(self):
        args = json.loads('[3]')
        kwargs = json.loads('{"b":5}')
        ret = json.loads('8')
        self.assertEqual(dealer.call(u'sum', args=args, kwargs=kwargs), ret)

    def test_call_sum_akw(self):
        args = json.loads('[3,5]')
        ret = json.loads('8')
        self.assertEqual(dealer.call(u'sum', args=args), ret)

    def test_call_list(self):
        kwargs = json.loads('{"b":null,"a":3,"c":"code","d":0.5}')
        ret = json.loads('[3, null,"code",0.5]')
        self.assertEqual(dealer.call(u'list', kwargs=kwargs), ret)

    def test_call_list_kw(self):
        args = json.loads('[3,null]')
        kwargs = json.loads('{"d":0.5,"c":"code"}')
        ret = json.loads('[3,null,"code",0.5]')
        self.assertEqual(dealer.call(u'list', args=args, kwargs=kwargs), ret)

    def test_call_dict(self):
        kwargs = json.loads('{"key":"a","value":34}')
        ret = json.loads('{"a":34}')
        self.assertEqual(dealer.call(u'dict', kwargs=kwargs), ret)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
