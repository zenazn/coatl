from django.db import models

class YNField(models.BooleanField):
    """
    It's like a boolean field, but it stores stuff in the database as 'y' and
    'n' (N is '-')
    """

    __metaclass__ = models.SubfieldBase

    def db_type(self):
        return 'char(1)'

    def to_python(self, value):
        if isinstance(value, bool):
            return value

        if value.lower() == 'y':
            return True
        else:
            return False

    def get_db_prep_value(self, value):
        if value:
            return 'y'
        else:
            return 'n'
