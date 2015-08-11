from django.db import models
from django.utils.translation import ugettext_lazy
from users.models import EntityLogin

class Moneyer(models.Model):
    
    MONEY_CATEGORY = (
        (1, ugettext_lazy('Income')),
        (2, ugettext_lazy('Food')),
        (3, ugettext_lazy('Traffic')),
        (4, ugettext_lazy('Movie')),
        (-1, ugettext_lazy('Other'))
    )
    
    owner = models.ForeignKey(EntityLogin, null = True, blank = True)
    money_category = models.SmallIntegerField('Money Category', choices = MONEY_CATEGORY, null = True, blank = True)
    credit = models.DecimalField('Credit', decimal_places = 2, max_digits = 10, null = True, blank = True)
    debit = models.DecimalField('Debit', decimal_places = 2, max_digits = 10, null = True, blank = True)
    remarks = models.TextField('Remarks', null = True, blank = True)
    create_date = models.DateField('Create Date', null = True, blank = True)
    
    class Meta:
        app_label = 'moneyer'
        db_table = 'moneyer_manager'
        
    def __unicode__(self):
        return '%s %s' % (self.owner.full_name, self.remarks)
    
