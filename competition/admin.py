from django.contrib import admin
import models

class RoundAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Round, RoundAdmin)


class ProblemAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Problem, ProblemAdmin)
