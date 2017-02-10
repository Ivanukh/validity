"""

All of comparators are inherited from :class:`.BaseComparator`.

This means that any of :ref:`available_comparators` has
:meth:`.Base.or_valid`,
:meth:`.Base.and_valid`,
:meth:`.Base.invert` **methods**,
that warp's comparator in :ref:`available_logical_operators`, so it is possible to building validators like this::

    EQ(42).or_valid(EQ(33))  # same as Or(EQ(42), (EQ(33))


Also they inherits other useful methods:

    - common validation methods:

        - :meth:`.all_is_valid`
        - :meth:`.get_error`
        - :meth:`.filter_values`

    - logical wrappers:

        - :meth:`~.Base.or_valid`
        - :meth:`~.Base.and_valid`
        - :meth:`~.Base.invert`

    - binary logic operations:

        - **|**  ( :meth:`~.Base.__or__` )
        - **&**  (:meth:`~.Base.__and__` )
        - **~**  ( :meth:`~.Base.__invert__` )


.. _available_comparators:

Available comparators
=====================


+----------------------------+--------------------------------------------------------------------------------+
|     class                  |   description                                                                  |
+============================+================================================================================+
| :class:`.GT`               | **greater than** *operand*.                                                    |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.GTE`              | **greater than or equal to** *operand*.                                        |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.LT`               | **less than** *operand*.                                                       |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.LTE`              | **less than or equal to** *operand*.                                           |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.EQ`               | **equal to** *operand*.                                                        |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.NotEQ`            | **not equal to** comparator.                                                   |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Any`              | **any from list** comparator.                                                  |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Between`          | **between min and max values** comparator.                                     |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.TypeIs`           | **check value type**                                                           |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.IsNone`           | **check if value is None**                                                     |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Len`              | **check length**                                                               |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Count`            | **check elements count**                                                       |
+----------------------------+--------------------------------------------------------------------------------+

.. TODO::

    add examples

"""

__docformat__ = 'reStructuredText'


from validity.logical_operator import Base


class BaseComparator(Base):
    """Base comparator class.
    Use it for creating other comparators.

    *Example*::

        >>> class IsDividableFor(BaseComparator):
        ...     _condition_template = "value must be dividable by {operand}"
        ...     def is_valid(self, value):
        ...         return value % self.operand == 0
        ...
        >>> cmp_1 = IsDividableFor(10)
        >>> cmp_1.is_valid(11)  # same as cmp_1(11)
        False
        >>> print cmp_1.get_condition_text()  # same as print cmp_1
        value must be dividable by 10
        >>>
        >>> cmp_1.operand = 2
        >>> print cmp_1.get_condition_text()
        value must be dividable by 2
        >>> cmp_1.filter_values(*range(1, 20))
        ([2, 4, 6, 8, 10, 12, 14, 16, 18], [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
        >>>
        >>> IsDividableFor(2).or_valid(IsDividableFor(3)).filter_values(*range(1,20))
        ([2, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18], [1, 5, 7, 11, 13, 17, 19])
        >>>
        >>> cmp_2 = IsDividableFor(2).or_valid(IsDividableFor(3).and_valid(NotEQ(9))).or_valid(EQ(7))
        >>> print cmp_2
        (value must be dividable by 2) OR ((value must be dividable by 3) AND (must NOT be equal to 9)) OR (must be equal to 7)
        >>> cmp_2.filter_values(*range(1,20))
        ([2, 3, 4, 6, 7, 8, 10, 12, 14, 15, 16, 18], [1, 5, 9, 11, 13, 17, 19])


    .. todo: docstring for Or, And, Not

    """

    _condition_template = 'Base comparator. operand={operand}'
    """Condition template, used for creating text representation of comparator (see :meth:`get_condition_text`)
    Must contains {operand} placeholder, if :meth:`get_condition_text` is not implemented in child class.
    """

    operand = None
    """Operand to compare with when :py:meth:`is_valid` called.
    Initial value must be given in :py:meth:`__init__`
    """

    def __init__(self, operand):
        """comparator initialization.

        :param operand: value to compare with when :py:meth:`is_valid` called

        """
        self.operand = operand

    def is_valid(self, value):
        """
        Check if given value is valid.

        .. warning::
            At :class:`.BaseComparator` class call to :meth:`is_valid` always raises `NotImplementedError`.
            Each child class **must** override this method
            and return :py:class:`bool` validation result

        :param value: value for validating
        :return: True if value is valid, otherwise - False
        :rtype: bool

        :raises ~exceptions.NotImplementedError: child class must implement 'is_valid(self, value)' method
        """
        raise NotImplementedError("comparator must implement 'is_valid(self, value)' method")

    def get_condition_text(self):
        """
        Get comparison condition text representation.
        Formats :attr:`._condition_template` with :attr:`operand` and returns result.

        :return: condition text representation (:attr:`_condition_template`.format(operand=self.operand))
        :rtype: str
        """
        # return self._condition_template.format(operand=self.operand)
        return self._condition_template.format(
            operand=("`{}`" if isinstance(self.operand, (str, )) else "{}").format(self.operand))


class GT(BaseComparator):
    """
    **Greater then comparator.**
    Use it for check that value > :attr:`operand`.

    example::

        >>> from validity import GT
        >>>
        >>> GT(10).is_valid(20)  # check if 20 is greater than 10
        True
        >>> test = GT(42)
        >>> test.is_valid(30)  # check if 30 is greater than 42
        False
        >>> test(30) # same as test.is_valid(30)
        False
        >>> test.get_condition_text()  # get text condition that describes comparator
        'must be greater than 42'
        >>>
        >>> test.filter_values(*range(40, 50))
        ([43, 44, 45, 46, 47, 48, 49], [40, 41, 42])
        >>> test.all_is_valid(10, 20, 300)  # check if all of [10, 20, 300] is greater than 42
        False
        >>> test.all_is_valid(43, 44, 45) # check if all of [43, 44, 45] is greater than 42
        True
        >>> print GT(20).or_valid(GT(10).invert())
        (must be greater than 20) OR NOT(must be greater than 10)
        >>> GT(20).or_valid(GT(10).invert()).all_is_valid(-100, 8, 9, 21, 22, 100)
        True

    """

    _condition_template = "must be greater than {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is greater than :attr:`operand`

        :param value: value for check
        :return: True if `value` > **self.operand** else False
        :rtype: bool
        """
        return value > self.operand


class GTE(BaseComparator):
    """
    **Greater then or equal to comparator.**
    Use it for check that value >= :attr:`operand`.

    Example::

        >>> from validity import GTE
        >>>
        >>> GTE(10).is_valid(20)  # check if 20 is greater than or equal to 10
        True
        >>> GTE(10).is_valid(10)  # check if 20 is greater than or equal to 10
        True
        >>> test = GTE(42)
        >>> test.get_condition_text()  # get text condition that describes comparator
        'must be greater than or equal to 42'
        >>>
        >>> test.filter_values(*range(40, 50))
        ([42, 43, 44, 45, 46, 47, 48, 49], [40, 41])

    """

    _condition_template = "must be greater than or equal to {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is greater than or equal to :attr:`operand`

        :param value: value for check
        :return: True if `value` >= **self.operand** else False
        :rtype: bool
        """
        return value >= self.operand


class LT(BaseComparator):
    """
    **Less then comparator.**
    Use it for check that value < :attr:`operand`.

    example::

        >>> from validity import LT
        >>>
        >>> LT(10).is_valid(5)  # check if 5 is less than 10
        True
        >>> test = LT(42)
        >>> test.is_valid(50)  # check if 50 is less than 42
        False
        >>> test(30) # same as test.is_valid(30)
        True
        >>> test.get_condition_text()  # get text condition that describes comparator
        'must be less than 42'
        >>>
        >>> test.filter_values(*range(40, 50))
        ([40, 41], [42, 43, 44, 45, 46, 47, 48, 49])
        >>> test.all_is_valid(10, 20, 300)  # check if all of [10, 20, 300] is less than 42
        False
        >>> test.all_is_valid(33, 34, 35) # check if all of [33, 34, 35] is less than 42
        True
        >>> print LT(10).or_valid(LT(20).invert())
        (must be less than 10) OR NOT(must be less than 20)
        >>> LT(10).or_valid(LT(20).invert()).all_is_valid(-100, 8, 9, 21, 22, 100)
        True

    """
    _condition_template = "must be less than {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is less than :attr:`operand`

        :param value: value for check
        :return: True if `value` < **self.operand** else False
        :rtype: bool
        """
        return value < self.operand


class LTE(BaseComparator):
    """
    **Less then or equal to comparator.**
    Use it for check that value <= :attr:`operand`.

    Example::

        >>> from validity import LTE
        >>>
        >>> LTE(10).is_valid(20)  # check if 20 is less than or equal to 10
        False
        >>> LTE(10).is_valid(10)  # check if 20 is less than or equal to 10
        True
        >>> test = LTE(42)
        >>> test.get_condition_text()  # get text condition that describes comparator
        'must be less than or equal to 42'
        >>>
        >>> test.filter_values(*range(40, 50))
        ([40, 41, 42], [43, 44, 45, 46, 47, 48, 49])

    """

    _condition_template = "must be less than or equal to {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is less than or equal to :attr:`operand`

        :param value: value for check
        :return: True if `value` <= **self.operand** else False
        :rtype: bool
        """
        return value <= self.operand


class EQ(BaseComparator):
    """
    **Equal to comparator**
    Use it for check that value == operand

    Example::

        >>> from validity import EQ
        >>>
        >>> EQ(10).is_valid(50)
        False
        >>> print EQ(10).get_error(50)
        must be equal to 10
        >>> print EQ(10).get_error(10)
        None
        >>> valid, not_valid = EQ(42).filter_values(*range(40, 45))
        >>> print valid
        [42]
        >>> print not_valid
        [40, 41, 43, 44]
        >>> print EQ(42) | EQ('forty two')
        (must be equal to 42) OR (must be equal to `forty two`)


    """
    _condition_template = "must be equal to {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        return value == self.operand


class NotEQ(BaseComparator):
    """
    NOT equal comparator
    Use it for check that value <> operand

    Example::

        >>> from validity import  NotEQ, Between
        >>>
        >>> NotEQ(10).is_valid(10)
        False
        >>> print NotEQ(10).get_error(10)
        must NOT be equal to 10
        >>> NotEQ(10).get_error(11)
        >>>
        >>> print Between(0, 20) & NotEQ(10) & NotEQ(11)
        (must be between 0 and 20) AND (must NOT be equal to 10) AND (must NOT be equal to 11)

    """

    _condition_template = "must NOT be equal to {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is not equal to :attr:`operand`

        :param value: value for check
        :return: True if `not value` == **self.operand** else False
        :rtype: bool
        """
        return not value == self.operand


class Any(BaseComparator):
    """
    **Any from list** comparator.
    Checks if given value is in list of allowed values.

    Example::

        >>> from validity import  Any
        >>>
        >>> print Any(10, 11, 12)
        must be any of (10, 11, 12)
        >>> allowed_values = [10, 11, 12]
        >>> print Any(allowed_values)  # same as Any(*allowed_values)
        must be any of (10, 11, 12)
        >>> Any("42", 42, "forty two").is_valid(42)
        True
        >>> Any("42", 42, "forty two").is_valid(-42)
        False
        >>> print Any(range(1, 5))
        must be any of (1, 2, 3, 4)

    """
    _condition_template = "must be any of ({operands})"
    """used for creating text representation of comparator (:py:meth:`get_condition_text`)"""

    def __init__(self, *values):
        """
        :param values: allowed values. If given only one value and it is instance of list or tuple, then it is used as list of valid values.
        :type values: list, tuple
        :raises ~exceptions.ValueError: if no validators specified

        """
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            if not values[0]:
                raise ValueError("at least one value must be specified")
            values = values[0]
        elif not values:
            raise ValueError("at least one value must be specified")
        super(Any, self).__init__(operand=values)

    def is_valid(self, value):
        """
        Check if given value in :attr:`operand`.

        :param value: value for check
        :return: True if value if list of allowed values, otherwise False
        :rtype: bool
        """
        return value in self.operand

    def get_condition_text(self):
        """
        Get condition text representation.
        Formats :attr:`._condition_template` with :attr:`operand` and returns result.
        Allowed  values are joined with coma.

        :return: condition text representation
        :rtype: str
        """
        return self._condition_template.format(operands=", ".join(str(item) for item in self.operand))

# just aliases
# In = Any
# AnyOf = In


class Between(BaseComparator):
    """
    **Between min_value and max_value comparator.**
    Use it for check that min_value <= value <= max_value.
    min_value and max_value res stored in :attr:`operand` as tuple (min_value, max_value)

    Example::

        >>> from validity import Between
        >>>
        >>> Between(10, 20).is_valid(20)  # check if 20 is between 10 and 20
        True
        >>> Between(10, 20).is_valid(0)  # check if 0 is between 10 and 20
        False
        >>> test = Between(40, 42)
        >>> test.get_condition_text()  # get text condition that describes comparator
        'must be between 40 and 42'
        >>>
        >>> test.filter_values(*range(38, 45))
        ([40, 41, 42], [38, 39, 43, 44])

    """
    _condition_template = "must be between {min_value} and {max_value}"
    """used for creating text representation of comparator (:py:meth:`get_condition_text`)"""

    def __init__(self, min_value, max_value):
        """
        *min_value* and *max_value* res stored in :attr:`operand` as tuple (min_value, max_value)

        :param min_value: minimum available value
        :type min_value: int
        :param max_value: maximum available value
        :type max_value: int
        """
        super(Between, self).__init__(operand=(min_value, max_value))

    def is_valid(self, value):
        """
        Check that min_value <= value <= max_value.
        min_value and max_value res stored in :attr:`operand` as tuple (min_value, max_value)

        :param value: value for check
        :return: True if :attr:`operand` [0] <= value <= :attr:`operand` [1], otherwise False
        :rtype: bool
        """
        return self.operand[0] <= value <= self.operand[1]

    def get_condition_text(self):
        """
        Get condition text representation.
        Formats :attr:`._condition_template` with min_value and max_value, stored as tuple in :attr:`operand`.

        :return: validation condition text representation
        :rtype: str
        """
        return self._condition_template.format(min_value=self.operand[0], max_value=self.operand[1])


class TypeIs(BaseComparator):
    """
    **Value type comparator**
    Use it for check that value type is same as :attr:`operand`.

    Example::

        >>> from validity import TypeIs
        >>>
        >>> TypeIs(int).is_valid(20)  # check if type of `20` is int
        True
        >>> TypeIs(list).is_valid([1, 2, 3, 4, 5, False])
        True
        >>> TypeIs(int).is_valid('1')
        False
        >>> test = TypeIs(int) | TypeIs(str)
        >>> test.get_condition_text()  # get text condition that describes comparator
        '(must be int) OR (must be str)'
        >>> test.filter_values(1, 2, [1,2,3], '1', {'test': 'test'}, (1, 2))
        ([1, 2, '1'], [[1, 2, 3], {'test': 'test'}, (1, 2)])

    """

    _condition_template = "must be {operand}"
    """used for creating text representation of comparator (:py:meth:`get_condition_text`)"""

    def __init__(self, required_type):
        """
        required_type is stored in :attr:`operand`.

        :param required_type: type to compare with
        :type required_type: type
        :raises ~exceptions.ValueError: if required_type is not instance of :class:`type`
        """
        if not isinstance(required_type, type):
            raise ValueError("required_type must be instance of 'type'")
        super(TypeIs, self).__init__(operand=required_type)

    def is_valid(self, value):
        """
        Check if type of given value is same as :attr:`operand`

        :param value: value to check
        :return: True if value has type same as :attr:`operand`, otherwise False
        :rtype: bool
        """
        # pylint: disable=unidiomatic-typecheck
        return type(value) is self.operand

    def get_condition_text(self):
        """
        Get condition text representation.
        Formats :attr:`._condition_template` with name of type, stored in :attr:`operand` and returns result.

        :return: condition text representation
        :rtype: str
        """
        return self._condition_template.format(operand=self.operand.__name__)


class IsNone(BaseComparator):
    """
    **Check that value is None**

    Example::

        >>> from validity import IsNone
        >>>
        >>> IsNone().is_valid(20)  # check if type of `20` is int
        False
        >>> IsNone().is_valid([])
        False
        >>> IsNone().is_valid(None)
        True
        >>> print IsNone()
        must be None
        >>> test = IsNone("there is not sense to be not None")
        >>> print test.get_condition_text()
        there is not sense to be not None
        >>> test.filter_values(1, '2', 3, 4, 5, None, 6, [], {})
        ([None], [1, '2', 3, 4, 5, 6, [], {}])
        >>> (~test).filter_values(1, '2', 3, 4, 5, None, 6, [], {})
        ([1, '2', 3, 4, 5, 6, [], {}], [None])

    """

    _condition_text = 'must be None'
    """used for creating text representation of comparator (:py:meth:`get_condition_text`)"""

    def __init__(self, condition_text=None):
        """
        It is possible to override default test representation with custom text from param condition_text

        :param condition_text: if given, default text representation will be overrided with it.
        :type condition_text:  str
        """
        super(IsNone, self).__init__(None)
        if condition_text:
            self._condition_text = condition_text

    def is_valid(self, value):
        """
        Check if given value is None

        :param value: value to check
        :return: True if value is None, otherwise False
        :rtype: bool
        """
        return value is None

    def get_condition_text(self):
        """
        Get condition text representation.
        It is possible to override default test representation while creating comparator (see :meth:`__init__`).

        :return: condition text representation
        :rtype: str
        """
        return self._condition_text or ''


class Len(BaseComparator):
    """
    Length validator.

    Example::

        >>> from validity import Len, GT, LT, EQ, Between
        >>>
        >>> print Len(Between(2, 5))
        length must be between 2 and 5
        >>> test = Len(Between(2, 5) | EQ(7))
        >>> print test
        length (must be between 2 and 5) OR (must be equal to 7)
        >>> test.is_valid("123")
        True
        >>> test.is_valid(123)
        False
        >>> print test | EQ("some extra unique possible value")
        (length (must be between 2 and 5) OR (must be equal to 7)) OR (must be equal to `some extra unique possible value`)
        >>> test |= Any("extra_const_value_1", "42", "other_possible_value")
        >>> test.filter_values('a', 'abc', '123456', '42')
        (['abc', '42'], ['a', '123456'])

    """
    _condition_template = "length {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, validator):
        """
        validator is stored in :attr:`operand`

        :param validator: any validator that will be used while validating value
        :type validator: Base
        :raises ~exceptions.ValueError: if validator is not instance of Base
        """
        if not isinstance(validator, Base):
            raise ValueError("validator must be instances of validity.Base class")

        super(Len, self).__init__(operand=validator)

    def is_valid(self, value):
        """
        Check if given value has length that is valid for :attr:`operand`.
        First step is to get value length. If length for value can not be calculated (for example, type of value is int), False is returned.
        Second step is to check if value length is valid for validator, sotred in :attr:`operand` (see :meth:`__init__`)

        :param value: value for length validation
        :return: True if length of value is valid for :attr:`operand` (see :meth:`__init__`), otherwise False
        :rtype: bool
        """
        try:
            value_length = len(value)
        except TypeError:
            return False
        return self.operand.is_valid(value_length)


class Count(Len):
    """
    Count validator.
    Same as len, except :attr:`_condition_template`

    Example::

        >>> from validity import Count, GT, LT, EQ, Between
        >>>
        >>> print Count(Between(2, 5))
        items count must be between 2 and 5
        >>> test = Count(Between(2, 5) | EQ(7))
        >>> print test
        items count (must be between 2 and 5) OR (must be equal to 7)
        >>> test.is_valid([1, 2, 3])
        True
        >>> test.is_valid([1, ])
        False
        >>> test.filter_values(['a', 'b'], ['a', 'b', 'c'], ['1', '2', '3', '4', '5', '6'])
        ([['a', 'b'], ['a', 'b', 'c']], [['1', '2', '3', '4', '5', '6']])

    """

    _condition_template = "items count {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""
