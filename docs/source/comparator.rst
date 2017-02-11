

Comparators
===========

.. automodule:: validity.comparator

.. py:currentmodule:: validity


GT (greater then comparator)
----------------------------

.. autoclass:: GT

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


GTE (greater then or equal to comparator)
-----------------------------------------

.. autoclass:: GTE

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`

LT (less than comparator)
-------------------------


.. autoclass:: LT

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`

LTE (less than or equal to comparator)
--------------------------------------

.. autoclass:: LTE

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`

EQ (equal to comparator)
------------------------

.. autoclass:: EQ

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


NotEQ (not equal to comparator)
-------------------------------

.. autoclass:: NotEQ

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


Any (any from list comparator)
------------------------------

.. autoclass:: Any

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_condition_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Base.__call__`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


Between (between min and max values comparator)
-----------------------------------------------

.. autoclass:: Between

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_condition_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseComparator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


TypeIs (check value type)
-------------------------


.. autoclass:: TypeIs

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_condition_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Base.__call__`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


IsNone (check if value is None)
-------------------------------

.. autoclass:: IsNone

    .. autoattribute:: _condition_text
    .. autoattribute:: operand

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_condition_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`



Len (check length)
------------------

.. autoclass:: Len

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. automethod:: __init__
    .. automethod:: is_valid

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`



Count (check elements count)
----------------------------

.. autoclass:: Count

    .. autoattribute:: _condition_template
    .. autoattribute:: operand

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Len.__init__`
            - :meth:`~.Len.is_valid`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseComparator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`
