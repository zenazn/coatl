from django.db import models
import fields

SCORE_CHOICES = (
    ('1', 'Correct'),
    ('0', 'Incorrect'),
    ('-', 'Blank'),
)

class Lock(models.Model):
    scorer = models.ForeignKey('User', db_column='scorerid', null=True)
    round = models.ForeignKey('competition.Round', db_column='roundid', null=True)
    solver = models.ForeignKey('registration.Mathlete', db_column='solverid', null=True)
    start = fields.TimestampField(auto_now=True)
    end = models.DateTimeField(null=True)

    class Meta:
        db_table = 'locks'

class Message(models.Model):
    scorer = models.ForeignKey('User', db_column='scorerid', null=True)
    msg = models.TextField(null=True)
    time = fields.TimestampField(auto_now=True)

    class Meta:
        db_table = 'messages'

class Score(models.Model):
    problem = models.ForeignKey('competition.Problem', db_column='problemid', null=True)
    solver = models.ForeignKey('registration.Mathlete', db_column='solverid', null=True)
    result = models.CharField(max_length=1, choices=SCORE_CHOICES, null=True)
    time = fields.TimestampField(auto_now=True)
    scorer = models.ForeignKey('User', db_column='scorerid', null=True)

    class Meta:
        db_table = 'scores'

class Update(models.Model):
    round = models.ForeignKey('competition.Round', db_column='roundid', null=True)
    solver = models.ForeignKey('registration.Mathlete', db_column='solverid', null=True)
    color = models.IntegerField(null=True)
    time = fields.TimestampField(auto_now=True)

    class Meta:
        db_table = 'updates'



class User(models.Model):
    login = models.CharField(max_length=64, null=True, unique=True)
    password = models.CharField(max_length=64, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
