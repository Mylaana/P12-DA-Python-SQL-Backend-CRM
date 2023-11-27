from django.contrib import admin
from UserProfile import models

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "phone",
                    "is_active", "is_admin", "is_staff",)


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id","name")

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Team, TeamAdmin)
