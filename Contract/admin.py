from django.contrib import admin
from Contract import models

class ContractAdmin(admin.ModelAdmin):

admin.site.register(models.Contract, ContractAdmin)