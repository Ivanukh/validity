
.. _base_classes:

Base validity classes
=====================

.. py:currentmodule:: validity


Base class
----------

.. autoclass:: validity.Base

    .. automethod:: __call__
    .. automethod:: is_valid
    .. automethod:: all_is_valid
    .. automethod:: get_error
    .. automethod:: filter_values
    .. automethod:: get_condition_text
    .. automethod:: get_nested_condition
    .. automethod:: __str__
    .. automethod:: __or__
    .. automethod:: or_valid
    .. automethod:: __and__
    .. automethod:: and_valid
    .. automethod:: __invert__
    .. automethod:: invert


BaseComparator
--------------

.. autoclass:: validity.BaseComparator

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


BaseLogicalOperator
-------------------

.. autoclass:: validity.BaseLogicalOperator

    .. autoattribute:: _condition_template
    .. autoattribute:: operands

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_condition_text
    .. automethod:: get_operands_text

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


.. TODO::

    ::

        def __or__(self, other):
            if type(self) == Or:
                return Or(*(self.operands + (other, )))
            return Or(self, other)

        def __and__(self, other):
            if type(self) == And:
                return And(*(self.operands + (other, )))
            return And(self, other)

        def __invert__(self):
            return Not(self)
