from django.contrib import admin
from gantter.models import Project, Task, TaskDependency

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)

class TaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)

class TaskDependencyAdmin(admin.ModelAdmin):
    pass

admin.site.register(TaskDependency, TaskDependencyAdmin)