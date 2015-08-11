from django.contrib import admin
from scheduler.models import Category, Event

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class EventAdmin(admin.ModelAdmin):
    pass

admin.site.register(Event, EventAdmin)