import unittest
from validity.comparator import GT, GTE, LT, LTE, EQ, NotEQ
from validity.logical_operator import Or, And


class TestGT(unittest.TestCase):

    def test_is_valid(self):
        comparator = GT(10)
        self.assertFalse(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid(11))

    def test_or(self):
        self.assertIsInstance(GT(10).Or(GT(20)), Or)

    def test_and(self):
        self.assertIsInstance(GT(10).And(GT(20)), And)

    def __str__(self):
        return "tests for comparator.GT (greater than comparator)"


class TestGTE(unittest.TestCase):

    def test_is_valid(self):
        comparator = GTE(10)
        self.assertFalse(comparator.is_valid(0))
        self.assertTrue(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid(11))

    def test_or(self):
        self.assertIsInstance(GTE(10).Or(GTE(20)), Or)

    def test_and(self):
        self.assertIsInstance(GTE(10).And(GTE(20)), And)

    def __str__(self):
        return "tests for comparator.GTE (greater or equal comparator)"


class TestLT(unittest.TestCase):

    def test_is_valid(self):
        comparator = LT(10)
        self.assertTrue(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(11))

    def test_or(self):
        self.assertIsInstance(LT(10).Or(LT(20)), Or)

    def test_and(self):
        self.assertIsInstance(LT(10).And(LT(20)), And)

    def __str__(self):
        return "tests for comparator.LT (less than comparator)"


class TestLTE(unittest.TestCase):

    def test_is_valid(self):
        comparator = LTE(10)
        self.assertTrue(comparator.is_valid(0))
        self.assertTrue(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(11))

    def __str__(self):
        return "tests for comparator.LTE (less than or equal comparator)"


class TestEQ(unittest.TestCase):

    def test_is_valid(self):
        comparator = EQ(10)
        self.assertFalse(comparator.is_valid(0))
        self.assertTrue(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid('10'))
        self.assertFalse(comparator.is_valid(False))
        self.assertFalse(comparator.is_valid(None))

        comparator = EQ('10')
        self.assertFalse(comparator.is_valid(0))
        self.assertTrue(comparator.is_valid('10'))
        self.assertFalse(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(False))
        self.assertFalse(comparator.is_valid(None))

        comparator = EQ(None)
        self.assertFalse(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid('10'))
        self.assertFalse(comparator.is_valid(False))
        self.assertTrue(comparator.is_valid(None))

    def test_or(self):
        self.assertIsInstance(EQ(10).Or(EQ(20)), Or)

    def test_and(self):
        self.assertIsInstance(EQ(10).And(EQ(20)), And)
        self.assertFalse(EQ(10).And(EQ(20)).is_valid(10))
        self.assertTrue(EQ(10).Or(EQ(20)).is_valid(10))

    def __str__(self):
        return "tests for comparator.EQ (equal comparator)"


class TestNotEQ(unittest.TestCase):

    def test_is_valid(self):
        comparator = NotEQ(10)
        self.assertTrue(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid('10'))
        self.assertTrue(comparator.is_valid(False))
        self.assertTrue(comparator.is_valid(None))

        comparator = NotEQ('10')
        self.assertTrue(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid('10'))
        self.assertTrue(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid(False))
        self.assertTrue(comparator.is_valid(None))

        comparator = NotEQ(None)
        self.assertTrue(comparator.is_valid(0))
        self.assertTrue(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid('10'))
        self.assertTrue(comparator.is_valid(False))
        self.assertFalse(comparator.is_valid(None))

    def test_or(self):
        self.assertIsInstance(NotEQ(10).Or(NotEQ(20)), Or)

    def test_and(self):
        self.assertIsInstance(NotEQ(10).And(NotEQ(20)), And)
        self.assertFalse(NotEQ(10).And(NotEQ(20)).is_valid(10))
        self.assertFalse(NotEQ(10).And(NotEQ(20)).is_valid(20))
        self.assertTrue(NotEQ(10).And(NotEQ(20)).is_valid(0))
        self.assertTrue(NotEQ(10).And(NotEQ(20)).is_valid(25))

    def __str__(self):
        return "tests for comparator.NotEQ (not equal comparator)"
