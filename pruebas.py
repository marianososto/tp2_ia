import unittest
import random


class MyTestCase(unittest.TestCase):
    def test_something(self):
        rnd = random.uniform(0, 100)
        print("hola", rnd)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
