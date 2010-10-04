from django.contrib import admin
import models

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type', 'paid', 'payment', 'comment')
    list_filter = ('paid', 'school_type')
    search_fields = ('name', 'comment')

admin.site.register(models.School, SchoolAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname', 'division', 'school', 'proctor', 'room', 'comment')
    list_filter = ('division', 'school')
    search_fields = ('name', 'shortname', 'school__name', 'proctor', 'room', 'comment')

admin.site.register(models.Team, TeamAdmin)

class MathleteAdmin(admin.ModelAdmin):
    list_display = ('first', 'last', 'alias', 'school', 'round1', 'round2', 'comment')
    list_filter = ('round1', 'round2', 'school')
    search_fields = ('first', 'last', 'alias', 'school__name', 'comment')

admin.site.register(models.Mathlete, MathleteAdmin)
