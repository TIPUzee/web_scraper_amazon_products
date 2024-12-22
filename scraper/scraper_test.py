import unittest
from .scraper import fetch_data

class MyTestCase(unittest.TestCase):
    def test_fetch_data(self):
        fetch_data('headphones')
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
