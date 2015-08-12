from django.db import models
from django.utils.translation import ugettext_lazy
from users.models import EntityLogin


class Category(models.Model):
    name = models.TextField('Category Name', null = True, blank = True)
    name_zhcn = models.TextField('Category Name (ZHCN)', null = True, blank = True)
    color = models.CharField('Category color', max_length = 64, null = True, blank = True)
    
    class Meta:
        app_label = 'scheduler'
        db_table = 'scheduler_category'
        
    def __unicode__(self):
        return self.name
    
    
class Event(models.Model):
    
    category = models.ForeignKey(Category, null = True, blank = True)
    
    owner = models.ForeignKey(EntityLogin, null = True, blank = True)
    title = models.TextField('Title', null = True, blank = True)
    start_date = models.DateField('Start Date', null = True, blank = True, help_text = 'Blank if not all day event')
    start_date_time = models.DateTimeField('Start Time', null = True, blank = True)
    to_date = models.DateField('To Date', null = True, blank = True)
    to_date_time = models.DateTimeField('To Time', null = True, blank = True)
    start_time_zone = models.CharField('Start Timezone', blank = True, null = True, max_length = 128)
    end_time_zone = models.CharField('End Timezone', blank = True, null = True, max_length = 128);
    recurrenceID = models.CharField('Recurrence ID', max_length = 128, blank = True, null = True)
    recurrenceRule = models.TextField('Recurrence Rule', null = True, blank = True)
    recurrenceException = models.TextField('Recurrence Exception', null = True, blank = True)
    isAllDay = models.BooleanField('Is all day', default = False)
    description = models.TextField('Description', null = True, blank = True)
    
    class Meta:
        app_label = 'scheduler'
        db_table = 'scheduler_event'
        
    def __unicode__(self):
        return '%s %s' % (self.category.name, self.title)
