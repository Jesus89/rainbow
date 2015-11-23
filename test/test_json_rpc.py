import json
import unittest
from rainbow import register
from rainbow.dealer import _call_manager as dealer


def jsonok(text):
    return json.dumps(json.loads(text))


class RainbowTest(unittest.TestCase):

    def setUp(self):
        # Register functions

        @register
        def subtract(minuend, subtrahend):
            return minuend - subtrahend

        @register
        def update(a, b, c, d, e):
            pass

        @register
        def foobar():
            pass

        @register
        def sum(a, b, c):
            return a + b + c

        @register
        def notify_sum(a, b, c):
            pass

        @register
        def notify_hello(a):
            pass

        @register
        def get_data():
            return ["hello", 5]

    def test_subtract_pos_params(self):
        request = '{"jsonrpc": "2.0","method": "subtract","params": [42, 23],"id": 1}'
        response = '{"jsonrpc": "2.0", "result": 19, "id": 1}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_subtract_named_params(self):
        request = '{"jsonrpc": "2.0", "method": "subtract", ' \
                  '"params": {"subtrahend": 23, "minuend": 42}, "id": 3}'
        response = '{"jsonrpc": "2.0", "result": 19, "id": 3}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_invalid_request_subtract(self):
        request = '{"method": "subtract","params": [42, 23],"id": 1}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_invalid_param_subtract(self):
        request = '{"jsonrpc": "2.0","method": "subtract","params": [42],"id": "id"}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32602, ' \
                   '"message": "Invalid params"}, "id": "id"}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_invalid_params_subtract(self):
        request = '{"jsonrpc": "2.0","method": "subtract","params": [42,"2"],"id": 1}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32602, ' \
                   '"message": "Invalid params"}, "id": 1}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_foobar(self):
        request = '{"jsonrpc": "2.0", "method": "foobar", "id": 1}'
        response = '{"jsonrpc": "2.0", "result": null, "id": 1}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_notification_update(self):
        request = '{"jsonrpc": "2.0", "method": "update", "params": [1,2,3,4,5]}'
        response = None
        self.assertEqual(dealer.process_request(request), response)

    def test_notification_foobar(self):
        request = '{"jsonrpc": "2.0", "method": "foobar"}'
        response = None
        self.assertEqual(dealer.process_request(request), response)

    def test_non_existent_method(self):
        request = '{"jsonrpc": "2.0", "method": "bar", "id": "1"}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32601, ' \
                   '"message": "Method not found"}, "id": "1"}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_invalid_json(self):
        request = '{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32700, ' \
                   '"message": "Parse error"}, "id": null}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_invalid_request(self):
        request = '{"jsonrpc": "2.0", "method": 1, "params": "bar"}'
        response = '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_batch_invalid_json(self):
        request = '[{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},' \
                  '{"jsonrpc": "2.0", "method"]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32700, ' \
                   '"message": "Parse error"}, "id": null}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_batch_emtpy_array(self):
        request = '[]'
        response = '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_batch_invalid_not_empty(self):
        request = '[1]'
        response = '[{"jsonrpc": "2.0", "error": {"code": -32600, ' \
                   '"message": "Invalid Request"}, "id": null}]'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_batch_invalid(self):
        request = '[1,2,3]'
        response = '[' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null},' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null},' \
            '{"jsonrpc": "2.0", "error": {"code": -32600, ' \
            '"message": "Invalid Request"}, "id": null}]'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_call_batch(self):
        request = '[' \
            '{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"},' \
            '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},' \
            '{"jsonrpc": "2.0", "method": "subtract", "params": [42,23], "id": "2"},' \
            '{"foo": "boo"},' \
            '{"jsonrpc": "2.0", "method": "foo.get", "params": {"name": "myself"}, "id": "5"},' \
            '{"jsonrpc": "2.0", "method": "get_data", "id": "9"}]'
        response = '[' \
            '{"jsonrpc": "2.0", "result": 7, "id": "1"},' \
            '{"jsonrpc": "2.0", "result": 19, "id": "2"},' \
            '{"jsonrpc": "2.0", "error":{"code": -32600, "message": "Invalid Request"}, ' \
            '"id": null},' \
            '{"jsonrpc": "2.0", "error":{"code": -32601, "message": "Method not found"}, ' \
            '"id": "5"},' \
            '{"jsonrpc": "2.0", "result": ["hello", 5], "id": "9"}]'
        self.assertEqual(dealer.process_request(request), jsonok(response))

    def test_call_batch_notification(self):
        request = '[{"jsonrpc": "2.0", "method": "notify_sum", "params": [1,2,4]},' \
                  '{"jsonrpc": "2.0", "method": "notify_hello", "params": [7]}]'
        response = None
        self.assertEqual(dealer.process_request(request), response)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
