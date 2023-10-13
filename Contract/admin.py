from django.contrib import admin
from Contract import models

class ContractAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Contract, ContractAdmin)