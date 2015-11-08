import unittest
from rainbow import app


# Register functions

@app.register('pi')
def pi():
    return 3.141592


@app.register('hello')
def hello(name):
    return 'Hello, ' + name


@app.register('sum')
def sum(a, b):
    return a + b


@app.register('list')
def _list(a, b, c):
    return [a, b, c]


@app.register('dict')
def _dict(key, value):
    ret = {}
    ret[key] = value
    return ret


class RainbowTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_sum(self):
        self.assertEqual(app.functions['sum'], sum)

    def test_call_pi(self):
        ret = '{"return":3.141592}'
        self.assertEqual(app.call('pi'), app.json_str(ret))

    def test_call_hello(self):
        params = '{"name":"world"}'
        ret = '{"return":"Hello, world"}'
        self.assertEqual(app.call('hello', params), app.json_str(ret))

    def test_call_sum(self):
        params = '{"a":3,"b":5}'
        ret = '{"return":8}'
        self.assertEqual(app.call('sum', params), app.json_str(ret))

    def test_call_list(self):
        params = '{"b":null,"a":3,"c":"code"}'
        ret = '{"return":[3, null,"code"]}'
        self.assertEqual(app.call('list', params), app.json_str(ret))

    def test_call_dict(self):
        params = '{"key":"a","value":34}'
        ret = '{"return":{"a":34}}'
        self.assertEqual(app.call('dict', params), app.json_str(ret))

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
