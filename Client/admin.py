from django.contrib import admin
from Client import models

class ClientAdmin(admin.ModelAdmin):
    list_display = ("ee_contact", "name", "siren", "email", "phone", "client_contact_name", "date_creation")


admin.site.register(models.Client, ClientAdmin)
