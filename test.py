import unittest
from time import sleep
from eoset import eoset


class TestExpireOrderedDict(unittest.TestCase):
    def setUp(self):
        self.set = eoset("blowglow")

    def test_contains(self):
        assert 'w' in self.set

    def test_getitem(self):
        self.assertEqual(self.set[3], 'w')

    def test_len(self):
        self.assertEqual(len(self.set), 5)

    def test_equal(self):
        self.assertEqual(self.set, eoset("blowg"))

    def test_reverse(self):
        self.assertEqual(eoset(reversed(self.set)), eoset("gwolb"))

    def test_pop(self):
        self.assertEqual(self.set.pop(), "b")
        self.assertEqual(self.set.pop_last(), "g")
        while len(self.set) > 0:
            self.set.pop()
        self.assertRaises(KeyError, self.set.pop)
        self.assertRaises(KeyError, self.set.pop_last)

    def test_expire(self):
        self.assertEqual(self.set.expire('p', 22), 0)
        self.set.expire('g', -999)
        self.assertEqual(self.set.ttl('g'), -1)
        self.set.expires(20)
        self.assertEqual(self.set.ttl('g'), 20)

        self.assertEqual(self.set.expire('o', 8), 1)
        self.assertAlmostEqual(self.set.ttl('o'), 8)

        sleep(10)
        self.assertAlmostEqual(self.set.ttl('o'), -2)

    def test_add_and_remove(self):
        self.set.add('x')
        self.assertEqual(len(self.set), 1)
        self.set.remove('x')
        self.assertEqual(len(self.set), 0)

    def test_by_order(self):
        self.test_contains()
        self.test_getitem()
        self.test_equal()
        self.test_reverse()
        self.test_expire()
        self.test_pop()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestExpireOrderedDict("test_by_order"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
