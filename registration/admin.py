from django.contrib import admin
import models

class MathleteInline(admin.TabularInline):
    model = models.Mathlete
    extra = 0
    exclude = ('school', 'comment',)

class TeamInline(admin.StackedInline):
    model = models.Team
    extra = 0
    exclude = ('comment',)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_type', 'paid', 'address', 'payment', 'team_count', 'comment')
    list_filter = ('paid', 'school_type')
    search_fields = ('name', 'comment')
    inlines = (TeamInline,)

admin.site.register(models.School, SchoolAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortname', 'division', 'school', 'proctor', 'room', 'mathlete_count', 'comment')
    list_filter = ('division', 'school')
    search_fields = ('name', 'shortname', 'school__name', 'proctor', 'room', 'comment')
    inlines = (MathleteInline,)

admin.site.register(models.Team, TeamAdmin)

class MathleteAdmin(admin.ModelAdmin):
    list_display = ('first', 'last', 'alias', 'school', 'round1', 'round2', 'comment')
    list_filter = ('round1', 'round2', 'school')
    search_fields = ('first', 'last', 'alias', 'school__name', 'team__name', 'team__shortname', 'comment')

admin.site.register(models.Mathlete, MathleteAdmin)
