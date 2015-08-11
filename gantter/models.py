from django.db import models
from django.utils.translation import ugettext_lazy
from users.models import EntityLogin

class Project(models.Model):
    
    owner = models.ForeignKey(EntityLogin, null = True, blank = True)
    title = models.TextField('Project Title', null = True, blank = True)
    description = models.TextField('Description', null = True, blank = True)
    color = models.CharField('Color', max_length = 64, null = True, blank = True)
    
    class Meta:
        app_label = 'gantter'
        db_table = 'gantter_project'
        
    def __unicode__(self):
        return '%s %s' % (self.owner.full_name, self.title)

class Task(models.Model):
    
    project = models.ForeignKey(Project, null = True, blank = True)
    parent = models.ForeignKey('self', null = True, blank = True)
    
    title = models.TextField('Title', null = True, blank = True)
    task_id = models.SmallIntegerField('Task ID', null = True, blank = True)
    order_id = models.SmallIntegerField('Order ID', null = True, blank = True)
    start = models.DateField('Start Date', null = True, blank = True)
    end = models.DateField('End Date', null = True, blank = True)
    percentage_complete = models.DecimalField('Percentage Completed', decimal_places = '2', max_digits = '5', null = True, blank = True)
    summary = models.BooleanField('Summary ?', default = True)
    expand = models.BooleanField('Expand ?', default = True)
    
    class Meta:
        app_label = 'gantter'
        db_table = 'gantter_task'
        
    def __unicode__(self):
        return '%s %s' % (self.project.title, self.title)

class TaskDependency(models.Model):
    
    predecessor = models.ForeignKey(Task, related_name = 'predecessor', null = True, blank = True)
    successor = models.ForeignKey(Task, related_name = 'successor', null = True, blank = True)
    dtype = models.SmallIntegerField('Type', null = True, blank = True)
    
    class Meta:
        app_label = 'gantter'
        db_table  = 'gantter_task_dependency'
        
    def __unicode__(self):
        return '%s depends on %s' % (self.successor.title, self.predecessor.title)
    