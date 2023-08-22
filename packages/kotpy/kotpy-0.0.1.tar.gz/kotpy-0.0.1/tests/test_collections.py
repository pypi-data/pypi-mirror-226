import unittest

from kotpy.collections import take_while, take_last_while


class CollectionTests(unittest.TestCase):
    def test_take_while(self):
        taken = take_while(range(1, 10), lambda n: n < 5)

        self.assertEqual([1, 2, 3, 4], taken)

    def test_take_last_while(self):
        taken = take_last_while(range(1, 10), lambda n: n > 5)

        self.assertEqual([6, 7, 8, 9], taken)
