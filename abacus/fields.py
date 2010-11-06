from django.db import models
from datetime import datetime
from time import strftime

# Lifted from http://ianrolfe.livejournal.com/36017.html
class TimestampField(models.DateTimeField):
    """
    It's just like a DateTimeField, but is backed by a 'timestamp' column in
    MySQL instead of a 'datetime' column.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(TimestampField, self).__init__(**kwargs)
        self.blank, self.isnull = blank, null
        # timestamps are 'not null' by default, so we have to correct for this
        self.null = True

    def db_type(self):
        t = ['timestamp']
        if self.isnull:
            t += ['NULL']
        if self.auto_now:
            t += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(t)

    def to_python(self, value):
        return datetime.from_timestamp(value)

    def get_db_prep_value(self, value):
        if value==None:
            return None
        return strftime('%Y%m%d%H%M%S', value.timetuple())
