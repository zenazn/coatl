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
    ('individual', _('Individual')),
    ('other', _('Other (E-mail us)')),
)

TEAM_DIVISIONS = (
    ('a', _('Division A')),
    ('b', _('Division B')),
)

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True)
    paid = models.BooleanField()
    comment = models.TextField(null=True)
    payment = models.FloatField()
    school_type = models.CharField(max_length=32, choices=SCHOOL_TYPES)
    
    coach = models.ForeignKey('auth.User')

    created = models.DateField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateField(auto_now=True, verbose_name=_('last updated at'))
    
    class Meta:
        db_table = 'schools'
    
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    shortname = models.CharField(max_length=15, help_text=_('Nickname for the guts round heads-up'), unique=True)
    school = models.ForeignKey('School', db_column='schoolid')
    comment = models.TextField(null=True)
    proctor = models.CharField(max_length=255)
    room = models.CharField(max_length=255)

    division = models.CharField(max_length=1, choices=TEAM_DIVISIONS)

    created = models.DateField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateField(auto_now=True, verbose_name=_('last updated at'))
    
    class Meta:
        db_table = 'teams'

class Mathlete(models.Model):
    first = models.CharField(max_length=60, verbose_name=_('first name'))
    last = models.CharField(max_length=60, verbose_name=_('last name'))
    alias = models.CharField(max_length=60, null=True, verbose_name=_('nickname'))
    
    school = models.ForeignKey('School', db_column='schoolid')
    team = models.ForeignKey('Team', db_column='teamid')
    
    round1 = models.ForeignKey('competition.Round', db_column='round1', related_name='mathelete_first_round_set', verbose_name=_('first round'))
    round2 = models.ForeignKey('competition.Round', db_column='round2', related_name='mathelete_second_round_set', verbose_name=_('second round'))

    regstatus = models.BooleanField(verbose_name=_('registration status'))

    comment = models.TextField(null=True)
    
    created = models.DateField(auto_now_add=True, verbose_name=_('created at'))
    lastupdate = models.DateField(auto_now=True, verbose_name=_('last updated at'))
    
    class Meta:
        db_table = 'mathletes'
