
.. _logical_operators:


Logical operators
=================

.. automodule:: validity.logical_operator


.. py:currentmodule:: validity

Or
--


.. autoclass:: Or

    .. autoattribute:: _condition_template
    .. autoattribute:: operands

    .. automethod:: is_valid
    .. automethod:: or_valid
    .. automethod:: get_operands_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseLogicalOperator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseLogicalOperator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`~.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`

And
---

.. autoclass:: And

    .. autoattribute:: _condition_template
    .. autoattribute:: operands

    .. automethod:: is_valid
    .. automethod:: and_valid
    .. automethod:: get_operands_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.BaseLogicalOperator.__init__`
            - :meth:`~.Base.__call__`
            - :meth:`~.BaseLogicalOperator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.get_nested_condition`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`


Not
---

.. autoclass:: Not

    .. autoattribute:: _condition_template
    .. autoattribute:: operands

    .. automethod:: __init__
    .. automethod:: is_valid
    .. automethod:: get_nested_condition
    .. automethod:: get_operands_text

    .. seealso::

        **Inherited methods**:

            - :meth:`~.Base.__call__`
            - :meth:`~.BaseLogicalOperator.get_condition_text`
            - :meth:`~.Base.all_is_valid`
            - :meth:`.Base.get_error`
            - :meth:`~.Base.filter_values`
            - :meth:`~.Base.__str__`
            - :meth:`~.Base.or_valid`
            - :meth:`~.Base.and_valid`
            - :meth:`~.Base.invert`

        **Inherited binary logic operations**

            - :meth:`~.Base.__or__`
            - :meth:`~.Base.__and__`
            - :meth:`~.Base.__invert__`
