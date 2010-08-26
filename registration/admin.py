from django.contrib import admin
from coatl.registration import models

class SchoolAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.School, SchoolAdmin)

class TeamAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Team, TeamAdmin)

class MathleteAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Mathlete, MathleteAdmin)
