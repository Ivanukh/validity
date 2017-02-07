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
    use it for check that value <> operand

    :example:

    NotEQ(10).is_valid(10)  # False
    NotEQ(10).get_error(10) # must NOT be equal to 10
    """

    _condition_template = "must NOT be equal to {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if given `value` is equal to :attr:`operand`

        :param value: value for check
        :return: True if `value` == **self.operand** else False
        :rtype: bool
        """
        return not value == self.operand


class Any(BaseComparator):

    _condition_template = "must be any of ({operands})"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, *values):
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = values[0]
        super(Any, self).__init__(operand=values)

    def is_valid(self, value):
        return value in self.operand

    def get_condition_text(self):
        return self._condition_template.format(operands=", ".join(str(item) for item in self.operand))

# just aliases
# In = Any
# AnyOf = In


class Between(BaseComparator):
    _condition_template = "must be between {min_value} and {max_value}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, min_value, max_value):
        super(Between, self).__init__(operand=(min_value, max_value))

    def is_valid(self, value):
        return self.operand[0] <= value <= self.operand[1]

    def get_condition_text(self):
        return self._condition_template.format(min_value=self.operand[0], max_value=self.operand[1])


class TypeIs(BaseComparator):
    _condition_template = "must be {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, required_type):
        if not isinstance(required_type, type):
            raise ValueError("required_type must be instance of 'type'")
        super(TypeIs, self).__init__(operand=required_type)

    def is_valid(self, value):
        # pylint: disable=unidiomatic-typecheck
        return type(value) is self.operand

    def get_condition_text(self):
        return self._condition_template.format(operand=self.operand.__name__)


class IsNone(BaseComparator):
    _condition_text = 'must be None'
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, condition_text=None):
        super(IsNone, self).__init__(None)
        if condition_text:
            self._condition_text = condition_text

    def is_valid(self, value):
        return value is None

    def get_condition_text(self):
        return self._condition_text or ''


class Len(BaseComparator):
    _condition_template = "length {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""

    def __init__(self, validator):
        if not isinstance(validator, Base):
            raise ValueError("validator must be instances of validity.Base class")

        super(Len, self).__init__(operand=validator)

    def is_valid(self, value):
        try:
            value_length = len(value)
        except TypeError:
            return False
        return self.operand.is_valid(value_length)

    def get_condition_text(self):
        return self._condition_template.format(operand=self.operand.get_condition_text())


class Count(Len):
    _condition_template = "items count {operand}"
    """used for creating text representation of comparator (:py:meth:`.BaseComparator.get_condition_text`)"""
