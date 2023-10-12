from django.contrib import admin
from UserProfile import models

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("team_name", "username", "email", "first_name", "last_name", "phone",
                    "is_active", "is_admin", "is_staff",)

    def team_name(self, obj):
        return obj.team.name

class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Team, TeamAdmin)
