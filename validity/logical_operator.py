"""

All logical operators extends :class:`.BaseLogicalOperator` class

This means that any of :ref:`available_logical_operators` has
:meth:`.or_valid`,
:meth:`.and_valid`,
:meth:`.invert` **methods**,
that warp's it self in other :ref:`available_logical_operators`, so it is possible to building validators like this::

    >>> from validity import And, GT, LT, EQ, NotEQ, Between, Not, TypeIs
    >>>
    >>> And(GT(0),  LT(33), NotEQ(15)).or_valid(EQ(42)).get_condition_text()
    '((must be greater than 0) AND (must be less than 33) AND (must NOT be equal to 15)) OR (must be equal to 42)'
    >>>
    >>> And(TypeIs(int), EQ(42)).or_valid(EQ('forty two')).get_condition_text()
    '((must be int) AND (must be equal to 42)) OR (must be equal to `forty two`)'
    >>>
    >>> working_hours = And(Between(9, 18), Not(Between(13,15))).or_valid(EQ(14))
    >>> print working_hours
    ((must be between 9 and 18) AND NOT(must be between 13 and 15)) OR (must be equal to 14)
    >>>
    >>> valid, not_valid = working_hours.filter_values(*range(0,24))
    >>> print "works    : {0}".format(valid)
    works    : [9, 10, 11, 12, 14, 16, 17, 18]
    >>> print "not works: {0}".format(not_valid)
    not works: [0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 15, 19, 20, 21, 22, 23]


Also they inherits other useful methods:

    - :meth:`.all_is_valid`
    - :meth:`.get_error`
    - :meth:`.filter_values`


.. _available_logical_operators:

Available logical operators
===========================

+--------------------------------+--------------------------------------------------------------------------------+
|     class                      |   description                                                                  |
+================================+================================================================================+
| :class:`.Or`                   | logical **or** for 2 or more *operands*                                        |
+--------------------------------+--------------------------------------------------------------------------------+
| :class:`.And`                  | logical **and** for 2 or more *operands*                                       |
+--------------------------------+--------------------------------------------------------------------------------+
| :class:`.Not`                  | logical **not** for single *operand*                                           |
+--------------------------------+--------------------------------------------------------------------------------+
| *operand* means instance of any class, inherited from any of :ref:`base_classes`:                               |
|                                                                                                                 |
| - :class:`.Base`                                                                                                |
| - :class:`.BaseComparator`                                                                                      |
| - :class:`.BaseLogicalOperator`                                                                                 |
|                                                                                                                 |
| This means that any of                                                                                          |
|                                                                                                                 |
| :ref:`comparator`, :ref:`logical_operator` can be used as *operand(s)* for any logical operator.                |
+-----------------------------------------------------------------------------------------------------------------+

.. TODO::

    add examples


"""


class Base(object):
    """
    Base class for all module classes.
    """

    def __call__(self, value):
        """
        If class instance is called like function - returns result of :meth:`.is_valid` method.

        Example::

            >>> from validity import Or, EQ, Between, Not
            >>> test = Or(EQ(42), EQ(0))
            >>> test(42)
            True
            >>> test(43)
            False
            >>> working_hours_checker = Between(9, 18).and_valid(Not(Between(13,14)))
            >>> working_hours_checker(20)
            False
            >>> working_hours_checker(17)
            True

        :param value: value for check
        :return: result of :meth:`.is_valid`
        :rtype: bool
        """
        return self.is_valid(value)

    def is_valid(self, value):
        """
        Check if given value is valid.

        .. warning::
            At :class:`.Base` class call to :meth:`.is_valid` always raises `NotImplementedError`.
            Each child class **must** override this method
            and return :py:class:`bool` validation result

        :param value: value for validating
        :return: True if value is valid, otherwise - False
        :rtype: bool
        """
        raise NotImplementedError()

    def all_is_valid(self, *values):
        """
        Checks if all of given values are valid

        :param values: values for check
        :return: True if result of :meth:`.is_valid` is True for all given values
        :rtype: bool
        """
        # return all(self.is_valid(value) for value in values)
        for value in values:
            if not self.is_valid(value):
                return False
        return True

    def get_error(self, value):
        """
        Get error text for given value if value is not valid ( :meth:`.is_valid` returned False).

        :param value: value for check.
        :return: None if :meth:`.is_valid` returned True, :meth:`.get_condition_text` in other cases.
        :rtype: None or str
        """
        return None if self.is_valid(value) else self.get_condition_text()

    def filter_values(self, *values):
        """
        Checks each given value and returns tuple of lists (valid, not_valid)

        :param values: values for check
        :return: ([list of valid values], [list of not valid values])
        :rtype: list, list
        """
        valid = []
        not_valid = []
        for value in values:
            (valid if self.is_valid(value) else not_valid).append(value)
        return valid, not_valid

    def get_condition_text(self):
        """
        Get validation condition text representation.

        :meth:`.get_error` returns result of this method if value is not valid

        .. warning::
            At :class:`.Base` class call to :meth:`.get_condition_text` always raises `NotImplementedError`.
            Each child class **must** override this method
            and return :py:class:`str` text representation of validation rule

        :return: validation condition text representation
        :rtype: str
        """
        raise NotImplementedError()

    def get_nested_condition(self):
        """
        Get validation condition, wrapped with brackets.

        Simple returns ({condition_text})

        This method is used by some other classes (like :class:`.And`, :class:`.Or`) when building self condition text

        :return: validation condition text representation, wrapped with brackets
        :rtype: str
        """
        return "({condition_text})".format(condition_text=self.get_condition_text())

    def __str__(self):
        """
        Text representation of class instance

        By default same as :meth:`.get_condition_text`

        :return: Text representation of class instance
        :rtype: str
        """
        return self.get_condition_text()

    def or_valid(self, *validators):
        """
        wraps ``self`` with :class:`Or` logical  comparator

        :param validators: :ref:`comparator` or :ref:`logical_operator` or any instance of :class:`Base` class
        :type validators: Base
        :return: joined with ``logical or`` self and validators (``Or(self, *validators)``)
        :rtype: Or
        """
        # pylint: disable=invalid-name
        if not len(validators):
            raise ValueError("at least one operand must be specified")
        return Or(self, *validators)

    def and_valid(self, *validators):
        """
        wraps ``self`` with :class:`And` logical  comparator

        :param validators: :ref:`comparator` , :ref:`logical_operator` or any instances of :class:`Base` class
        :type validators: Base
        :return: joined with ``logical and`` self and validators (``And(self, *validators)``)
        :rtype: And
        """
        # pylint: disable=invalid-name
        if not len(validators):
            raise ValueError("at least one operand must be specified")
        return And(self, *validators)

    def invert(self):
        """
        wraps ``self`` with :class:`Not` logical  comparator

        :return: ``Not(self)``
        :rtype: Not
        """
        return Not(self)


class BaseLogicalOperator(Base):
    """
    Base logical operator class
    """

    _condition_template = "base logical operator. always falls. operands={operands}"
    """Condition template, used for creating text representation of logical operator (see :meth:`get_condition_text`)
    Must contains {operands} placeholder, if :meth:`get_condition_text` is not implemented in child class.
    """

    operands = None
    """Operands to work with when :py:meth:`is_valid` called.
    One or more operands must be given in :py:meth:`__init__`
    """

    def __init__(self, *operands):
        """
        logical operator initialization


        :param operands: one or more operand to work with
        :type operands: Base
        :raises ~exceptions.ValueError: if no operands
        :raises ~exceptions.ValueError: if not all of operands is instances of :class:`.Base`
        """
        if not len(operands):
            raise ValueError("at least one operand must be specified")

        if not all([isinstance(operand, Base) for operand in operands]):
            raise ValueError("all operands must be instances of validity.Base class")

        self.operands = operands

    def is_valid(self, value):
        """
        Check value is valid.

        .. warning::
            At :class:`.BaseLogicalOperator` class call to :meth:`is_valid` always raises `NotImplementedError`.
            Each child class **must** override this method
            and return :py:class:`bool` validation result

        :param value: value for validating
        :return: True if value is valid, otherwise - False
        :rtype: bool

        :raises ~exceptions.NotImplementedError: child class must implement 'is_valid(self, value)' method
        """

        raise NotImplementedError("operator must implement 'is_valid(self, value)' method")

    def get_condition_text(self):
        """
        Get logical expression text representation.
        Formats :attr:`._condition_template` with :attr:`operands` and returns result.

        :return: logical expression text representation (:attr:`_condition_template`.format(operands= :meth:`get_operands_text` )
        :rtype: str
        """
        return self._condition_template.format(operands=self.get_operands_text())

    def get_operands_text(self):
        """
        Get :attr:`operands` text representation.
        Result is used in :meth:`get_condition_text` .

        :return: text representation of :attr:`operands`
        :rtype: str
        """
        return ", ".join([str(operand) for operand in self.operands])


class Or(BaseLogicalOperator):
    """
    Logical "Or" operator.

    *Example*::

        from validity import Or, EQ, GT, LT, Between

        Or(GT(20), EQ(42)).is_valid(10)
        # False
        test = Or(GT(20), EQ(42))
        test.get_condition_text()
        # (must be greater than 20) OR (must be equal to 42)

        test = Or(EQ(42), LT(33), Between(35, 40))
        test.get_condition_text()
        # (must be equal to 42) OR (must be less than 33) OR (must be between 35 and 40)

        valid, not_valid = test.filter_values(*range(32, 41))
        # [32, 35, 36, 37, 38, 39, 40], [33, 34]

        test.all_is_valid(42, 29, 35)
        # True

        test.or_valid(EQ(100), EQ(200)).get_condition_text()
        # ((must be equal to 42) OR (must be less than 33) OR (must be between 35 and 40)) OR ((must be equal to 100) OR (must be equal to 200))
        test.or_valid(EQ(100)).is_valid(100)
        # True

    """
    _condition_template = "{operands}"
    """Condition template, used for creating text representation (see :meth:`.BaseLogicalOperator.get_condition_text`)"""

    def is_valid(self, value):
        """
        Check if any of :attr:`operands` is valid for given value.
        Simply executes is_valid method in each of :attr:`operands`
        and returns True if any of :attr:`operands` is_valid method returned True

        :param value: value for check
        :type value:
        :return: True, if any operand from :attr:`operands` returned True in is_valid method,
            other wise returns False
        :rtype: bool
        """
        # return any([operand.is_valid(value) for operand in self.operands])
        for operand in self.operands:
            if operand.is_valid(value):
                return True
        return False

    def get_operands_text(self):
        """
        Get :attr:`operands` text representation.
        Result is used in :meth:`.BaseLogicalOperator.get_condition_text`.

        :return: text representation of :attr:`operands`, joined with `OR`
        :rtype: str
        """

        return " OR ".join([operand.get_nested_condition() for operand in self.operands])


class And(BaseLogicalOperator):
    """
        Logical "And" operator.

    *Example*::

        from validity import And, NotEQ, GT, LT, Between

        And(GT(20), LT(42)).is_valid(10)
        # False
        test = And(GT(20), LT(42))
        test.get_condition_text()
        # (must be greater than 20) AND (must be less than 42)

        test = And(NotEQ(42), NotEQ(43), Between(35, 45))
        test.get_condition_text()
        # (must NOT be equal to 42) AND (must NOT be equal to 43) AND (must be between 35 and 45)

        valid, not_valid = test.filter_values(*range(32, 47))
        # [35, 36, 37, 38, 39, 40, 41, 44, 45], [32, 33, 34, 42, 43, 46]

        test.all_is_valid(41, 35, 44, 45)
        # True

        test.or_valid(EQ(100), EQ(200)).get_condition_text()
        # ((must NOT be equal to 42) AND (must NOT be equal to 43) AND (must be between 35 and 45)) OR ((must be equal to 100) OR (must be equal to 200))
        test.or_valid(EQ(100)).is_valid(100)
        # True

    """
    _condition_template = "{operands}"

    def is_valid(self, value):
        return all([operand.is_valid(value) for operand in self.operands])

    def get_operands_text(self):
        return " AND ".join([operand.get_nested_condition() for operand in self.operands])


class Not(BaseLogicalOperator):
    _condition_template = "NOT({operands})"

    def __init__(self, condition):
        super(Not, self).__init__(condition)

    def is_valid(self, value):
        for operand in self.operands:
            if not operand.is_valid(value):
                return True
        return False

    def get_nested_condition(self):
        return self.get_condition_text()

    def get_operands_text(self):
        return str(self.operands[0])
