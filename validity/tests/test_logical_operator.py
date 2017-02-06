#pylint: skip-file
from unittest import TestCase
from validity.comparator import GT, LT, GTE, LTE, EQ, Any, Between, TypeIs
from validity.logical_operator import Base, BaseLogicalOperator, Or, And, Not


class TestBase(TestCase):

    def test_call_method(self):
        with self.assertRaises(NotImplementedError):
            Base().__call__(20)

    def test_get_error_method(self):
        with self.assertRaises(NotImplementedError):
            Base().get_error(42)

    def test_Or_method(self):
        self.assertIsInstance(Base().Or(GT(10)), Or)
        op1 = GT(10)
        op2 = GT(20)

        self.assertEqual(op1.Or(op2).operands[0], op1)
        self.assertEqual(op1.Or(op2).operands[1], op2)

        with self.assertRaises(ValueError):
            Base().Or()

    def test_And_method(self):
        self.assertIsInstance(Base().And(GT(10)), And)
        op1 = GT(10)
        op2 = GT(20)

        self.assertEqual(op1.And(op2).operands[0], op1)
        self.assertEqual(op1.And(op2).operands[1], op2)

        with self.assertRaises(ValueError):
            Base().And()

    def test_Not_method(self):
        self.assertIsInstance(Base().Not(), Not)
        op1 = GT(10)

        self.assertEqual(op1.Not().operands[0], op1)

    def test_filter_values(self):
        with self.assertRaises(NotImplementedError):
            Base().filter_values(1, 2, 3, 4, 5)

        valid, not_valid = GT(10).filter_values(*range(0, 20))
        self.assertEqual(not_valid, list(range(0, 11)))
        self.assertEqual(valid, list(range(11, 20)))

    def test_all_is_valid_method(self):
        with self.assertRaises(NotImplementedError):
            Base().all_is_valid(1, 2, 3, 4, 5)

        self.assertTrue(GT(10).all_is_valid(*range(100, 110)))
        self.assertFalse(GT(10).all_is_valid(*range(10, 20)))
        self.assertFalse(GT(10).all_is_valid(10, 11, 12))
        self.assertFalse(GT(10).all_is_valid(11, 20, 30, 0))

    def test_get_condition_text(self):
        with self.assertRaises(NotImplementedError):
            Base().get_condition_text()


class TestBaseLogicalOperator(TestCase):

    def test_constructor(self):
        with self.assertRaises(ValueError):
            BaseLogicalOperator()

        with self.assertRaises(ValueError):
            BaseLogicalOperator(1, 1)

        with self.assertRaises(ValueError):
            BaseLogicalOperator(GT(10), 1)

        cmp_1, cmp_2, cmp_3 = GT(42), GT(42), GT(42)
        operator = BaseLogicalOperator(cmp_1, cmp_2, cmp_3)
        self.assertEqual(operator.operands[0], cmp_1)
        self.assertEqual(operator.operands[1], cmp_2)
        self.assertEqual(operator.operands[2], cmp_3)

    def test_get_condition_text_method(self):
        self.assertEqual(BaseLogicalOperator(GT(10)).get_condition_text(),
                         'base logical operator. always falls. operands=must be greater than 10')
        self.assertEqual(BaseLogicalOperator(GT(10), LT(20)).get_condition_text(),
                         'base logical operator. always falls. operands=must be greater than 10, must be less than 20')

    def test_get_operands_text_method(self):
        self.assertEqual(BaseLogicalOperator(GT(10)).get_operands_text(),
                         'must be greater than 10')
        self.assertEqual(BaseLogicalOperator(GT(10), LT(20)).get_operands_text(),
                         'must be greater than 10, must be less than 20')

    def test_is_valid_method(self):
        with self.assertRaises(NotImplementedError):
            BaseLogicalOperator(GT(10)).is_valid(None)


class TestOr(TestCase):

    def test_is_valid(self):
        for comparator in[GT, LT, GTE, LTE, EQ]:
            cmp_1 = comparator(10)
            cmp_2 = comparator(20)
            cmp_3 = comparator(30)
            for value in range(0, 100):
                self.assertEqual(Or(cmp_1, cmp_2, cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) or cmp_2.is_valid(value) or cmp_3.is_valid(value))
                self.assertEqual(cmp_1.Or(cmp_2, cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) or cmp_2.is_valid(value) or cmp_3.is_valid(value))

                self.assertEqual(cmp_1.Or(cmp_2).Or(cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) or cmp_2.is_valid(value) or cmp_3.is_valid(value))
        cmp_1 = Between(0, 110)
        cmp_2 = Between(50, 150)
        for value in range(0, 120):
            self.assertEqual(Or(cmp_1, cmp_2).is_valid(value),
                             cmp_1.is_valid(value) or cmp_2.is_valid(value))

        cmp_1 = Any(range(0, 25))
        cmp_2 = Any(range(25, 50))
        cmp_3 = Any(range(75, 100))

        for value in range(0, 100):
            self.assertEqual(Or(cmp_1, cmp_2, cmp_3).is_valid(value),
                             cmp_1.is_valid(value) or cmp_2.is_valid(value) or cmp_3.is_valid(value))

        cmp_1 = TypeIs(int)
        cmp_2 = TypeIs(str)
        for value in [42, '42', [42, ], (42, )]:
            self.assertEqual(Or(cmp_1, cmp_2).is_valid(value),
                             cmp_1.is_valid(value) or cmp_2.is_valid(value))

    def test_get_operands_text_method(self):
        self.assertEqual(Or(GT(100), LT(0)).get_operands_text(),
                         '(must be greater than 100) OR (must be less than 0)')

        self.assertEqual(Or(GT(100), LT(0), EQ(42)).get_operands_text(),
                         '(must be greater than 100) OR (must be less than 0) OR (must be equal to 42)')


class TestAnd(TestCase):

    def test_is_valid(self):
        for comparator in[GT, LT, GTE, LTE, EQ]:
            cmp_1 = comparator(5)
            cmp_2 = comparator(15)
            cmp_3 = comparator(35)
            for value in range(0, 100):
                self.assertEqual(And(cmp_1, cmp_2, cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) and cmp_2.is_valid(value) and cmp_3.is_valid(value))
                self.assertEqual(cmp_1.And(cmp_2, cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) and cmp_2.is_valid(value) and cmp_3.is_valid(value))

                self.assertEqual(cmp_1.And(cmp_2).And(cmp_3).is_valid(value),
                                 cmp_1.is_valid(value) and cmp_2.is_valid(value) and cmp_3.is_valid(value))

        cmp_1 = Between(0, 100)
        cmp_2 = Between(50, 150)
        for value in range(0, 100):
            self.assertEqual(And(cmp_1, cmp_2).is_valid(value),
                             cmp_1.is_valid(value) and cmp_2.is_valid(value))

        cmp_1 = Any(range(0, 50))
        cmp_2 = Any(range(25, 50))
        cmp_3 = Any(range(30, 100))

        for value in range(0, 100):
            self.assertEqual(And(cmp_1, cmp_2, cmp_3).is_valid(value),
                             cmp_1.is_valid(value) and cmp_2.is_valid(value) and cmp_3.is_valid(value))

        cmp_1 = TypeIs(int)
        cmp_2 = TypeIs(int)
        for value in [42, '42', [42, ], (42,)]:
            self.assertEqual(And(cmp_1, cmp_2).is_valid(value),
                             cmp_1.is_valid(value) and cmp_2.is_valid(value))

    def test_get_operands_text_method(self):
        self.assertEqual(And(GT(0), LT(100)).get_operands_text(),
                         '(must be greater than 0) AND (must be less than 100)')

        self.assertEqual(And(GT(0), LT(100), EQ(42)).get_operands_text(),
                         '(must be greater than 0) AND (must be less than 100) AND (must be equal to 42)')


class TestNot(TestCase):

    def test_constructor(self):
        with self.assertRaises(TypeError):
            Not()

        with self.assertRaises(TypeError):
            Not(1, 1)

    def test_is_valid(self):
        # TODO: test for TypeIs
        for comparator in[GT, LT, GTE, LTE, EQ]:
            cmp_1 = comparator(20)
            for value in range(0, 100):
                self.assertEqual(Not(cmp_1).is_valid(value),
                                 not cmp_1.is_valid(value))
                self.assertEqual(cmp_1.Not().is_valid(value),
                                 not cmp_1.is_valid(value))

        cmp_1 = TypeIs(int)
        for value in [42, '42', [42, ], (42,)]:
            self.assertEqual(Not(cmp_1).is_valid(value),
                             not cmp_1.is_valid(value))
            self.assertEqual(cmp_1.Not().is_valid(value),
                             not cmp_1.is_valid(value))

    def test_get_operands_text_method(self):
        self.assertEqual(Not(GT(0)).get_operands_text(),
                         'must be greater than 0')

    def test_get_nested_condition_method(self):
        self.assertEqual(Not(GT(10)).get_condition_text(), Not(GT(10)).get_nested_condition())
