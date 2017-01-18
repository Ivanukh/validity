from unittest import TestCase
from validity.comparator import GT, LT, EQ
from validity.logical_operator import Or, And, Any, Between


class TestBetween(TestCase):

    def test_is_valid(self):
        comparator = Between(10, 20)
        self.assertTrue(comparator.is_valid(10))
        self.assertTrue(comparator.is_valid(20))
        self.assertTrue(comparator.is_valid(15))
        self.assertFalse(comparator.is_valid(9))
        self.assertFalse(comparator.is_valid(21))

    def test_or(self):
        comparator = Between(10, 20).Or(EQ(42))
        self.assertTrue(comparator.is_valid(42))
        self.assertFalse(comparator.is_valid(43))

    def test_and(self):
        comparator = Between(10, 20).And(GT(15))
        self.assertTrue(comparator.is_valid(16))
        self.assertFalse(comparator.is_valid(10))

    def __str__(self):
        return "tests for logical_operator.Between"


class TestOr(TestCase):

    def test_is_valid(self):
        comparator = Or(LT(10), GT(50), Between(20, 30))

        self.assertTrue(comparator.is_valid(9))
        self.assertFalse(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(15))

        self.assertFalse(comparator.is_valid(50))
        self.assertTrue(comparator.is_valid(51))

        self.assertFalse(comparator.is_valid(19))
        self.assertTrue(comparator.is_valid(20))
        self.assertTrue(comparator.is_valid(25))
        self.assertTrue(comparator.is_valid(30))
        self.assertFalse(comparator.is_valid(35))

    def test_or(self):
        comparator = Or(LT(10), GT(50), Between(20, 30)).Or(EQ(42))
        self.assertTrue(comparator.is_valid(42))

    def __str__(self):
        return "tests for logical_operator.Or"


class TestAnd(TestCase):

    def test_is_valid(self):
        comparator = And(GT(10), GT(20), GT(30), LT(40))

        self.assertTrue(comparator.is_valid(31))
        self.assertTrue(comparator.is_valid(35))
        self.assertFalse(comparator.is_valid(0))
        self.assertFalse(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(15))
        self.assertFalse(comparator.is_valid(20))
        self.assertFalse(comparator.is_valid(25))
        self.assertFalse(comparator.is_valid(30))
        self.assertFalse(comparator.is_valid(40))
        self.assertFalse(comparator.is_valid(41))

    def test_or(self):
        comparator = And(GT(10), GT(20), GT(30), LT(40)).Or(EQ(42))
        self.assertTrue(comparator.is_valid(42))

    def __str__(self):
        return "tests for logical_operator.And"


class TestAny(TestCase):

    def test_is_valid(self):
        comparator = Any(10, 20, 30, 'a', ['1', '2', '3'])

        self.assertTrue(comparator.is_valid(10))
        self.assertFalse(comparator.is_valid(11))
        self.assertTrue(comparator.is_valid('a'))
        self.assertFalse(comparator.is_valid('b'))

        self.assertFalse(comparator.is_valid(['1', '2']))
        self.assertFalse(comparator.is_valid(['1', '2', '4']))
        self.assertTrue(comparator.is_valid(['1', '2', '3']))

    def test_or(self):
        comparator = Any(10, 20, 30, 'a', ['1', '2', '3']).Or(EQ(42))
        self.assertTrue(comparator.is_valid(42))

    def __str__(self):
        return "tests for logical_operator.Any"
