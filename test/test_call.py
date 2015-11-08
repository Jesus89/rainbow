import unittest
from rainbow import app, register


class RainbowTest(unittest.TestCase):

    def setUp(self):
        # Register functions

        @register('pi')
        def pi():
            return 3.141592

        @register('hello')
        def hello(name):
            return 'Hello, ' + name

        @register('sum')
        def sum(a, b):
            return a + b

        @register('list')
        def _list(a, b, c, d):
            return [a, b, c, d]

        @register('dict')
        def _dict(key, value):
            ret = {}
            ret[key] = value
            return ret

    def test_call_pi(self):
        ret = '{"result":3.141592}'
        self.assertEqual(app.call('pi'), app.json_str(ret))

    def test_call_hello(self):
        args = '["world"]'
        ret = '{"result":"Hello, world"}'
        self.assertEqual(app.call('hello', args=args), app.json_str(ret))

    def test_call_hello_kw(self):
        kwargs = '{"name":"world"}'
        ret = '{"result":"Hello, world"}'
        self.assertEqual(app.call('hello', kwargs=kwargs), app.json_str(ret))

    def test_call_sum(self):
        kwargs = '{"a":3,"b":5}'
        ret = '{"result":8}'
        self.assertEqual(app.call('sum', kwargs=kwargs), app.json_str(ret))

    def test_call_sum_kw(self):
        args = '[3]'
        kwargs = '{"b":5}'
        ret = '{"result":8}'
        self.assertEqual(app.call('sum', args=args, kwargs=kwargs), app.json_str(ret))

    def test_call_sum_akw(self):
        args = '[3,5]'
        ret = '{"result":8}'
        self.assertEqual(app.call('sum', args=args), app.json_str(ret))

    def test_call_list(self):
        kwargs = '{"b":null,"a":3,"c":"code","d":0.5}'
        ret = '{"result":[3, null,"code",0.5]}'
        self.assertEqual(app.call('list', kwargs=kwargs), app.json_str(ret))

    def test_call_list_kw(self):
        args = '[3,null]'
        kwargs = '{"d":0.5,"c":"code"}'
        ret = '{"result":[3,null,"code",0.5]}'
        self.assertEqual(app.call('list', args=args, kwargs=kwargs), app.json_str(ret))

    def test_call_dict(self):
        kwargs = '{"key":"a","value":34}'
        ret = '{"result":{"a":34}}'
        self.assertEqual(app.call('dict', kwargs=kwargs), app.json_str(ret))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
