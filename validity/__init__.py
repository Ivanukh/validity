"""

Validity is module for validation created to help implement primitive and complex validation rules.
It implements :ref:`comparators` and :ref:`logical_operators`
Each of them extended from :class:`.Base` class and can be referred in documentation and examples as *validator*.


*validators* categories
~~~~~~~~~~~~~~~~~~~~~~~

    - :ref:`comparators` - primitive comparison classes, that can be used to compare given value with other value.
    - :ref:`logical_operators` - logical expression classes, that can be used for building higher level validation rules.


Validators, implemented in validity module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+----------------------------+--------------------------------------------------------------------------------+
| :ref:`comparators` - **primitive comparison classes, that can be used to compare given value                |
| with other value**                                                                                          |
+----------------------------+--------------------------------------------------------------------------------+
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
| :ref:`logical_operators` - **logical expression classes, that can be used for                               |
| building higher level validation rules**                                                                    |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Or`               | logical **or** for 2 or more *validators*                                      |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.And`              | logical **and** for 2 or more *validators*                                     |
+----------------------------+--------------------------------------------------------------------------------+
| :class:`.Not`              | logical **not** for single *validators*                                        |
+----------------------------+--------------------------------------------------------------------------------+
| *validator* means instance of any class, inherited from any of :ref:`base_classes`:                         |
|                                                                                                             |
| - :class:`.Base`                                                                                            |
| - :class:`.BaseComparator`                                                                                  |
| - :class:`.BaseLogicalOperator`                                                                             |
|                                                                                                             |
| Also, any of :ref:`logical_operators` can be userd as `validotor`.                                          |
| This means that any of                                                                                      |
|                                                                                                             |
| :ref:`comparators`, :ref:`logical_operators` can be used as *validator(s)* for any logical operator.        |
+-------------------------------------------------------------------------------------------------------------+


Main features of *validators*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    - Any *validator* has :meth:`~.Base.is_valid` method for check if value is valid.
    - Any *validator* can be wrapped with any of :ref:`logical_operators`.
    - Binary logical *or*, *and*, *invert* operations ( **|**, **&**, **~** ) can be used for creating logical conditions. ( like ``TypeIs(int) & (EQ(42) | EQ(55))`` )
    - Any *validator* can be called as function (see :meth:`~.Base.__call__`).
    - Any *validator* can check if all given values is valid with :meth:`~.Base.all_is_valid`.
    - Any *validator* can split pack of values to valid and not_valid lists with :meth:`~.Base.filter_values` method.
    - Any *validator* can be represented as human-readable logical condition with :meth:`~.Base.get_condition_text` method

Any validator extends one of :ref:`base_classes`. This means that all of validators implements:

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


Simple example
~~~~~~~~~~~~~~

::

    >>> from validity import GT, LT, EQ, Between
    >>>
    >>> GT(20).is_valid(50)  # check if 50 is greater than 20
    True
    >>> print GT(20)
    must be greater than 20
    >>> test = GT(50).or_valid(LT(40), EQ(42))  # same as GT(50) | LT(40) | EQ(42)
    >>> print test
    (must be greater than 50) OR (must be less than 40) OR (must be equal to 42)
    >>> test.filter_values(*range(38, 53))
    ([38, 39, 42, 51, 52], [40, 41, 43, 44, 45, 46, 47, 48, 49, 50])
    >>> print Between(0, 100) & (GT(50) | LT(40) | EQ(42))
    (must be between 0 and 100) AND ((must be greater than 50) OR (must be less than 40) OR (must be equal to 42))


More complex example
~~~~~~~~~~~~~~~~~~~~

::

    >>> from validity import And, GT, LT, EQ, NotEQ, Between, Not, TypeIs
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


.. seealso:: :ref:`base_classes` for example of creating custom validators.


"""

from validity.comparator import BaseComparator, \
    GT, GTE, LT, LTE, EQ, NotEQ, \
    Any, \
    Between, \
    TypeIs, IsNone, \
    Len, Count
from validity.logical_operator import Base, BaseLogicalOperator, Or, And, Not

__all__ = [
    # comparators
    'BaseComparator',
    'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NotEQ',
    'Any',
    'Between',
    'TypeIs', 'IsNone',
    'Len', 'Count',
    # logical operators
    'Base', 'BaseLogicalOperator', 'Or', 'And', 'Not']
