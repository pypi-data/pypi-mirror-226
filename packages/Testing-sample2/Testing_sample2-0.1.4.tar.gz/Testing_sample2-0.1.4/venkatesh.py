import unittest

class MyMath:
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def subtract(x, y):
        return x - y

# The test class
class TestMyMath(unittest.TestCase):

    def test_add(self):
        self.assertEqual(MyMath.add(2, 3), 5)
        self.assertEqual(MyMath.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(MyMath.subtract(5, 3), 2)
        self.assertEqual(MyMath.subtract(10, 5), 5)