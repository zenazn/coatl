from django.db import models
from django.contrib.auth import models as auth
from competition import models as competition
from django.utils.translation import ugettext_lazy as _

SCHOOL_TYPES = (
    ('private', _('Private School')),
    ('magnet', _('Magnet School')),
    ('regional', _('Regional School')),
    ('public_big', _('Large Public School')),
    ('public_small', _('Small Public School')),
    ('homeschool',_('Homeschooled')),
    ('individual', _('Individual')),
    ('other', _('Other (E-mail us)')),
)

TEAM_DIVISIONS = (
    ('a', _('Division A')),
    ('b', _('Division B')),
)

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    payment = models.FloatField(default=0)
    school_type = models.CharField(max_length=32, choices=SCHOOL_TYPES)

    coaches = models.ManyToManyField(auth.User, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateTimeField(auto_now=True, verbose_name=_('last updated at'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'schools'

class Team(models.Model):
    # Backwords compatibility sucks.
    number = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, unique=True)
    shortname = models.CharField(max_length=15, help_text=_('Nickname for the guts round scoreboard'), unique=True)
    school = models.ForeignKey('School', db_column='schoolid')
    comment = models.TextField(null=True, blank=True)
    proctor = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=255, blank=True)

    division = models.CharField(max_length=1, choices=TEAM_DIVISIONS)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateTimeField(auto_now=True, verbose_name=_('last updated at'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teams'

class Mathlete(models.Model):
    first = models.CharField(max_length=60, verbose_name=_('first name'))
    last = models.CharField(max_length=60, verbose_name=_('last name'))
    alias = models.CharField(max_length=60, null=True, blank=True, verbose_name=_('nickname'), help_text=_('Should we expect any other names written on the test?'))

    school = models.ForeignKey('School', db_column='schoolid')
    team = models.ForeignKey('Team', null=True, blank=True, db_column='teamid')

    round1 = models.ForeignKey('competition.Round', db_column='round1', related_name='mathelete_round1_set', verbose_name=_('first round'))
    round2 = models.ForeignKey('competition.Round', db_column='round2', related_name='mathelete_round2_set', verbose_name=_('second round'))

    regstatus = models.BooleanField(default=False,verbose_name=_('registration status'))

    comment = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateTimeField(auto_now=True, verbose_name=_('last updated at'))

    def __str__(self):
        if self.alias:
            return '%(first)s "%(alias)s" %(last)s' % self.__dict__
        else:
            return u'%(first)s %(last)s' % self.__dict__

    class Meta:
        db_table = 'mathletes'

