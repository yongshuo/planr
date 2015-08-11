from django.contrib import admin
from moneyer.models import Moneyer

class MoneyerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Moneyer, MoneyerAdmin)
