from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from UserProfile import models

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "phone",
                    "is_active", "is_admin", "is_staff", "team")


class TeamAdmin(admin.ModelAdmin):
    list_display = ("id","name")

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Team, TeamAdmin)
