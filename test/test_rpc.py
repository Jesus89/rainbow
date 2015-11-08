import unittest
from rainbow import app


# Setup app

@app.register('pi')
def pi():
    return 3.141592


@app.register('hello')
def hello(name):
    return 'Hello, ' + name


@app.register('sum')
def sum(a, b):
    return a + b


class RainbowTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_sum(self):
        self.assertEqual(app.functions['sum'], sum)

    def test_call_pi(self):
        ret = {}
        ret['return'] = pi()
        self.assertEqual(app.call('pi'), ret)

    def test_call_hello(self):
        name = 'world'
        params = {}
        params['name'] = name
        ret = {}
        ret['return'] = hello(name)
        self.assertEqual(app.call('hello', **params), ret)

    def test_call_sum(self):
        params = {}
        params['a'] = 3
        params['b'] = 5
        ret = {}
        ret['return'] = 8
        self.assertEqual(app.call('sum', **params), ret)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
