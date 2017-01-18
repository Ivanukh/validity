from .logical_operator import Or, And
from .base import Base


class BaseComparator(Base):
    condition_template = "base comparator"
    operand = None

    def __init__(self, operand, condition_template=None):
        self.operand = operand
        if condition_template is not None:
            self.condition_template = condition_template

    def get_error_message(self, value):
        return self.condition_template.format(operand=self.operand) + ". {} given".format(value)

    def get_condition(self):
        return self.condition_template.format(operand=self.operand)

    def Or(self, *args):
        # pylint: disable=invalid-name
        # TODO check args
        return Or(self, *args)

    def And(self, *args):
        # pylint: disable=invalid-name
        # TODO check args
        return And(self, *args)


class GT(BaseComparator):
    condition_template = "must be greater than {operand}"

    def is_valid(self, value):
        return value > self.operand


class GTE(BaseComparator):
    condition_template = "must be greater than or equal to {operand}"

    def is_valid(self, value):
        return value >= self.operand


class LT(BaseComparator):
    condition_template = "must be less than {operand}"

    def is_valid(self, value):
        return value < self.operand


class LTE(BaseComparator):
    condition_template = "must be less than or equal to {operand}"

    def is_valid(self, value):
        return value <= self.operand


class EQ(BaseComparator):
    condition_template = "must be equal to {operand}"

    def is_valid(self, value):
        return value == self.operand


class NotEQ(BaseComparator):
    condition_template = "must NOT be equal to {operand}"

    def is_valid(self, value):
        return not value == self.operand
