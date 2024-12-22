import unittest
from .reader import load_json


class MyTestCase(unittest.TestCase):
    def test_load_json(self):
        data = load_json('user_queries.json')
        self.assertEqual(['headphones', 'smartphones'], data)


if __name__ == '__main__':
    unittest.main()
