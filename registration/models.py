from django.db import models
from django.contrib.auth import models as auth
from competition import models as competition

SCHOOL_TYPES = (
    ('private', 'Private School'),
    ('magnet', 'Magnet School'),
    ('regional', 'Regional School'),
    ('public_big', 'Large Public School'),
    ('public_small', 'Small Public School'),
    ('individual', 'Individual'),
    ('other', 'Other (E-mail us)'),
)

TEAM_DIVISIONS = (
    ('a', 'Division A'),
    ('b', 'Division B'),
)

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True)
    paid = models.BooleanField()
    comment = models.TextField(null=True)
    payment = models.FloatField()
    school_type = models.CharField(max_length=32, choices=SCHOOL_TYPES)
    
    coach = models.ForeignKey('auth.User')

    created = models.DateField(auto_now_add=True, verbose_name="created at")
    lastupdate = models.DateField(auto_now=True, verbose_name="last updated at")
    
    class Meta:
        db_table = 'schools'
    
class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    shortname = models.CharField(max_length=15, help_text="Nickname for the guts round heads-up", unique=True)
    school = models.ForeignKey('School', db_column='schoolid')
    comment = models.TextField(null=True)
    proctor = models.CharField(max_length=255)
    room = models.CharField(max_length=255)

    division = models.CharField(max_length=1, choices=TEAM_DIVISIONS)

    created = models.DateField(auto_now_add=True, verbose_name="created at")
    lastupdate = models.DateField(auto_now=True, verbose_name="last updated at")
    
    class Meta:
        db_table = 'teams'

class Mathlete(models.Model):
    first = models.CharField(max_length=60, verbose_name="first name")
    last = models.CharField(max_length=60, verbose_name="last name")
    alias = models.CharField(max_length=60, null=True, verbose_name="nickname")
    
    school = models.ForeignKey('School', db_column='schoolid')
    team = models.ForeignKey('Team', db_column='teamid')
    
    round1 = models.ForeignKey('competition.Round', db_column='round1', related_name='mathelete_first_round_set', verbose_name="first round")
    round2 = models.ForeignKey('competition.Round', db_column='round2', related_name='mathelete_second_round_set', verbose_name="second round")

    regstatus = models.BooleanField(verbose_name="registration status")

    comment = models.TextField(null=True)
    
    created = models.DateField(auto_now_add=True, verbose_name="created at")
    lastupdate = models.DateField(auto_now=True, verbose_name="last updated at")
    
    class Meta:
        db_table = 'mathletes'
