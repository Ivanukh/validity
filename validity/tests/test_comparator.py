#pylint: skip-file
from unittest import TestCase
from validity.comparator import BaseComparator, GT, GTE, LT, LTE, EQ, NotEQ, Any, Between, TypeIs, IsNone, Len, Count


class TestBaseComparator(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            BaseComparator()

        with self.assertRaises(TypeError):
            BaseComparator(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(BaseComparator(None).get_condition_text(), 'Base comparator. operand=None')
        self.assertEqual(BaseComparator("test").get_condition_text(), 'Base comparator. operand=`test`')

    def test_is_valid_method(self):
        with self.assertRaises(NotImplementedError):
            BaseComparator(None).is_valid(None)


class TestGT(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            GT()

        with self.assertRaises(TypeError):
            GT(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(GT(10).get_condition_text(), 'must be greater than 10')
        self.assertEqual(GT(100).get_condition_text(), 'must be greater than 100')

    def test_is_valid_method(self):
        self.assertFalse(GT(10).is_valid(10))
        self.assertTrue(GT(10).is_valid(20))

        self.assertFalse(GT(10).is_valid(0))
        self.assertFalse(GT(10).is_valid(-10))


class TestGTE(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            GTE()

        with self.assertRaises(TypeError):
            GTE(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(GTE(10).get_condition_text(), 'must be greater than or equal to 10')
        self.assertEqual(GTE(100).get_condition_text(), 'must be greater than or equal to 100')

    def test_is_valid_method(self):
        self.assertFalse(GTE(10).is_valid(9))
        self.assertTrue(GTE(10).is_valid(10))
        self.assertTrue(GTE(10).is_valid(20))

        self.assertFalse(GTE(10).is_valid(0))
        self.assertFalse(GTE(10).is_valid(-10))


class TestLT(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            LT()

        with self.assertRaises(TypeError):
            LT(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(LT(10).get_condition_text(), 'must be less than 10')
        self.assertEqual(LT(100).get_condition_text(), 'must be less than 100')

    def test_is_valid_method(self):
        self.assertFalse(LT(10).is_valid(10))
        self.assertFalse(LT(10).is_valid(20))

        self.assertTrue(LT(10).is_valid(0))
        self.assertTrue(LT(10).is_valid(-10))


class TestLTE(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            LTE()

        with self.assertRaises(TypeError):
            LTE(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(LTE(10).get_condition_text(), 'must be less than or equal to 10')
        self.assertEqual(LTE(100).get_condition_text(), 'must be less than or equal to 100')

    def test_is_valid_method(self):
        self.assertTrue(LTE(10).is_valid(9))
        self.assertTrue(LTE(10).is_valid(10))
        self.assertFalse(LTE(10).is_valid(20))

        self.assertTrue(LTE(10).is_valid(0))
        self.assertTrue(LTE(10).is_valid(-10))


class TestEQ(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            EQ()

        with self.assertRaises(TypeError):
            EQ(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(EQ(10).get_condition_text(), 'must be equal to 10')
        self.assertEqual(EQ(100).get_condition_text(), 'must be equal to 100')
        self.assertEqual(EQ('100').get_condition_text(), 'must be equal to `100`')

    def test_is_valid_method(self):
        self.assertFalse(EQ(10).is_valid(9))
        self.assertFalse(EQ(10).is_valid('10'))
        self.assertTrue(EQ(10).is_valid(10))


class TestNotEQ(TestCase):
    def test_constructor(self):
        with self.assertRaises(TypeError):
            NotEQ()

        with self.assertRaises(TypeError):
            NotEQ(1, 1)

    def test_get_condition_text_method(self):
        self.assertEqual(NotEQ(10).get_condition_text(), 'must NOT be equal to 10')
        self.assertEqual(NotEQ(100).get_condition_text(), 'must NOT be equal to 100')

    def test_is_valid_method(self):
        self.assertTrue(NotEQ(10).is_valid(9))
        self.assertTrue(NotEQ(10).is_valid('10'))
        self.assertFalse(NotEQ(10).is_valid(10))


class TestAny(TestCase):

    def test_constructor(self):
        with self.assertRaises(ValueError):
            Any()
        with self.assertRaises(ValueError):
            Any([])

        self.assertEqual(Any(1).operand[0], 1)
        self.assertEqual(len(Any(1).operand), 1)

        self.assertEqual(Any(1, 2).operand[0], 1)
        self.assertEqual(Any(1, 2).operand[1], 2)
        self.assertEqual(len(Any(1, 2).operand), 2)

        self.assertEqual(Any([1, 2]).operand[0], 1)
        self.assertEqual(Any([1, 2]).operand[1], 2)
        self.assertEqual(len(Any([1, 2]).operand), 2)

    def test_get_condition_text_method(self):
        self.assertEqual(Any(10).get_condition_text(), 'must be any of (10)')
        self.assertEqual(Any(10, 42).get_condition_text(), 'must be any of (10, 42)')
        self.assertEqual(Any([10, 42]).get_condition_text(), 'must be any of (10, 42)')

    def test_is_valid_method(self):
        self.assertTrue(Any(10, 42).is_valid(10))
        self.assertTrue(Any(10, 42).is_valid(42))
        self.assertFalse(Any(10, 42).is_valid(0))


class TestBetween(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            Between()

        with self.assertRaises(TypeError):
            LTE(1, 1, 1)

        self.assertEqual(Between(10, 42).operand[0], 10)
        self.assertEqual(Between(10, 42).operand[1], 42)
        self.assertEqual(len(Between(10, 42).operand), 2)

    def test_get_condition_text_method(self):
        self.assertEqual(Between(10, 42).get_condition_text(), 'must be between 10 and 42')
        self.assertEqual(Between(1, 142).get_condition_text(), 'must be between 1 and 142')

    def test_is_valid_method(self):
        self.assertTrue(Between(10, 42).is_valid(10))
        self.assertTrue(Between(10, 42).is_valid(42))
        self.assertTrue(Between(10, 42).is_valid(20))
        self.assertFalse(Between(10, 42).is_valid(0))
        self.assertFalse(Between(10, 42).is_valid(50))


class TestTypeIs(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            TypeIs()

        with self.assertRaises(TypeError):
            TypeIs(1, 2)

        with self.assertRaises(ValueError):
            TypeIs(1)

        self.assertEqual(TypeIs(int).operand, int)
        self.assertEqual(TypeIs(str).operand, str)

    def test_get_condition_text_method(self):
        self.assertEqual(TypeIs(int).get_condition_text(), 'must be int')
        self.assertEqual(TypeIs(str).get_condition_text(), 'must be str')

    def test_is_valid_method(self):
        self.assertTrue(TypeIs(int).is_valid(42))
        test_variable = 42
        self.assertTrue(TypeIs(int).is_valid(test_variable))
        self.assertTrue(TypeIs(str).is_valid('42'))
        self.assertTrue(TypeIs(tuple).is_valid((0, 42,)))
        self.assertTrue(TypeIs(list).is_valid([0, 42,]))

        self.assertFalse(TypeIs(int).is_valid('42'))
        self.assertFalse(TypeIs(str).is_valid(42))
        self.assertFalse(TypeIs(tuple).is_valid(42))
        self.assertFalse(TypeIs(tuple).is_valid([0, 42]))
        self.assertFalse(TypeIs(list).is_valid((0, 42,)))


class TestIsNone(TestCase):

    def test_constructor(self):
        self.assertIsInstance(IsNone(), IsNone)
        self.assertIsInstance(IsNone('must be none'), IsNone)

    def test_is_valid_method(self):
        self.assertFalse(IsNone().is_valid(42))
        self.assertFalse(IsNone().is_valid('42'))
        self.assertFalse(IsNone().is_valid([]))
        self.assertFalse(IsNone().is_valid({}))
        self.assertFalse(IsNone().is_valid((None, None, )))
        self.assertTrue(IsNone().is_valid(None))

    def test_get_condition_text_method(self):
        self.assertEqual(IsNone().get_condition_text(), 'must be None')
        self.assertEqual(IsNone('None').get_condition_text(), 'None')


class TestLen(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            Len()

        with self.assertRaises(TypeError):
            Len(1, 2)

        with self.assertRaises(ValueError):
            Len(1)

        for comparator in [GT, GTE, LT, LTE]:
            validator = comparator(42)
            self.assertEqual(Len(validator).operand, validator)

    def test_get_condition_text_method(self):
        self.assertEqual(Len(EQ(42)).get_condition_text(), 'length must be equal to 42')
        self.assertEqual(Len(Between(1, 50)).get_condition_text(), 'length must be between 1 and 50')
        self.assertEqual(Len(GT(1).and_valid(LT(10))).get_condition_text(), 'length (must be greater than 1) AND (must be less than 10)')

    def test_is_valid_method(self):
        self.assertFalse(Len(Between(1, 5)).is_valid(''))
        self.assertTrue(Len(Between(1, 5)).is_valid('1'))
        self.assertTrue(Len(Between(1, 5)).is_valid('12'))
        self.assertTrue(Len(Between(1, 5)).is_valid('12345'))
        self.assertFalse(Len(Between(1, 5)).is_valid('123456'))

        self.assertFalse(Len(Between(1, 5)).is_valid([]))
        self.assertFalse(Len(Between(1, 5)).is_valid(1))
        self.assertTrue(Len(Between(1, 5)).is_valid([1, ]))
        self.assertTrue(Len(Between(1, 5)).is_valid([1, 2, 3]))
        self.assertTrue(Len(Between(1, 5)).is_valid([1, 2, 3, 4, 5]))
        self.assertFalse(Len(Between(1, 5)).is_valid([1, 2, 3, 4, 5, 6]))


class TestCount(TestCase):

    def test_get_condition_text_method(self):
        self.assertEqual(Count(EQ(42)).get_condition_text(), 'items count must be equal to 42')
        self.assertEqual(Count(Between(1, 50)).get_condition_text(), 'items count must be between 1 and 50')
        self.assertEqual(Count(GT(1).and_valid(LT(10))).get_condition_text(),
                         'items count (must be greater than 1) AND (must be less than 10)')
