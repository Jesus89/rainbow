import unittest
import rainbow


class RainbowTest(unittest.TestCase):

    def setUp(self):
        self.app = rainbow.app

    def test_test(self):
        self.assertEqual(self.app, self.app)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
