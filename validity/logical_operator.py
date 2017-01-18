from .base import Base


class BaseLogicalOperator(Base):
    condition_template = "base logical operator. always falls"

    def Or(self, *args):
        # pylint: disable=invalid-name
        return Or(self, *args)

    def And(self, *args):
        # pylint: disable=invalid-name
        return And(self, *args)


class TwoArgsLogicalOperator(BaseLogicalOperator):
    condition_template = "base two args logical operator. always falls"

    operand_1 = None
    operand_2 = None

    def __init__(self, operand_1, operand_2, condition_template=None):
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        if condition_template is not None:
            self.condition_template = condition_template

    def get_error_message(self, value):
        return self.condition_template.format(operand_1=self.operand_1, operand_2=self.operand_2) + ", {} given".format(
            value)

    def get_condition(self):
        return self.condition_template.format(operand_1=self.operand_1, operand_2=self.operand_2)


class Between(TwoArgsLogicalOperator):
    condition_template = "must be between {operand_1} and {operand_2}"

    def is_valid(self, value):
        return self.operand_1 <= value <= self.operand_2


# TODO: and

class BaseMultiOperand(BaseLogicalOperator):
    operands = None
    error_template = "{operands}"
    operands_join_str = ";"
    description_template = "{operands}"

    def __init__(self, *args):
        self.operands = args

    def get_error_message(self, value):
        return self.error_template.format(
            operands=self.operands_join_str.join(["({})".format(operand) for operand in self.operands])) + ", {} given".format(value)

    def get_condition(self):
        return self.description_template.format(
            operands=self.operands_join_str.join([str(operand) for operand in self.operands]))


class Or(BaseMultiOperand):
    operands_join_str = " OR "

    def is_valid(self, value):
        return any([operand.is_valid(value) for operand in self.operands])


class Any(BaseMultiOperand):
    # TODO: rename to In ?
    error_template = "must be any of ({operands})"
    operands_join_str = ";"
    description_template = "must be any of ({operands})"

    operands_join_str = "; "

    def is_valid(self, value):
        return any([operand == value for operand in self.operands])


class And(BaseMultiOperand):
    operands_join_str = " AND "

    def is_valid(self, value):
        return all([operand.is_valid(value) for operand in self.operands])
