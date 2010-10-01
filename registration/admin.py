from django.contrib import admin
from coatl.registration import models

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type', 'paid', 'payment', 'comment')
    list_filter = ('paid', 'school_type')

admin.site.register(models.School, SchoolAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname', 'division', 'school', 'proctor', 'room', 'comment')
    list_filter = ('division', 'school')

admin.site.register(models.Team, TeamAdmin)

class MathleteAdmin(admin.ModelAdmin):
    list_display = ('first', 'last', 'alias', 'school', 'round1', 'round2', 'comment')
    list_filter = ('round1', 'round2', 'school')

admin.site.register(models.Mathlete, MathleteAdmin)
