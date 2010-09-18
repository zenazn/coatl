from django.db import models

GROUP_CHOICES = (
    ('general', "General"),
    ('subject', "Subject"),
    ('team', "Team Round")
)

class Round(models.Model):
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=10, choices=GROUP_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'rounds'

class Problem(models.Model):
    round = models.ForeignKey('Round')
    number = models.IntegerField(verbose_name="Problem Number")
    points = models.IntegerField()
    
    statement = models.TextField()
    answer = models.TextField()
    solution = models.TextField() 

    def __str__(self):
        return "%s Question %d" % (self.round.name, self.number)
    
    class Meta:
        db_table = 'problems'
