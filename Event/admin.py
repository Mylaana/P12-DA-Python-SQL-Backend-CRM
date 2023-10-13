from django.contrib import admin
from Event import models

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Event, EventAdmin)

