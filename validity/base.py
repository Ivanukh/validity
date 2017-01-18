

class Base(object):
    condition_template = 'base comparator. always falls'

    def get_error(self, value):
        is_ok, error = self.check(value)
        if is_ok:
            return None
        return error

    def is_valid(self, value):
        return False

    def check(self, value):
        is_valid = self.is_valid(value)
        return is_valid, None if is_valid else self.get_error_message(value)

    def __str__(self):
        return self.get_condition()

    def __unicode__(self):
        return self.get_condition()

    def get_error_message(self, value):
        return self.condition_template

    def get_condition(self):
        return self.condition_template