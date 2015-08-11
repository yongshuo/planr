from django.db import models
from django.contrib.auth.hashers import check_password, make_password, mask_hash
from django.utils.translation import ugettext_lazy

class EntityLogin(models.Model):
    
    ENTITY_STATUS = (
        (1, ugettext_lazy('Active')),
        (-1, ugettext_lazy('Inactive')),
        (-2, ugettext_lazy('Deleted'))
    )
    
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = -1
    STATUS_DELETED = -2
    
    full_name = models.CharField('full name', max_length = 128, null = True, blank = True)
    search_text = models.CharField('search text', max_length = 1024, null = True, blank = True)
    email = models.CharField('email', max_length = 128, blank = True, null = True)
    password_hash = models.CharField('Hashed password', max_length = 128, blank = True, null = True)
    status = models.SmallIntegerField('status', choices = ENTITY_STATUS, null = True, blank = True, default = STATUS_ACTIVE)
    activation_code = models.CharField('Activation Code', max_length = 128, null = True, blank = True, help_text = 'Used for activating account by the activation link')
    create_time = models.DateTimeField('create time', auto_now_add = True)
    
    class Meta:
        app_label = 'users'
        db_table = 'users_entitylogin'
        
    def __unicode__(self):
        return '%s %s' % (self.full_name, self.email)
    
    @property
    def password(self):
        return mask_hash(self.password_hash)
    
    @password.setter
    def password(self, value):
        self.password_hash = make_password(value)
    
    def verify_password(self, value):
        return check_password(value, self.password_hash)
    
    @staticmethod
    def get_user_by_email(email):
        try:
            entity_login = EntityLogin.objects.get(email = email)
        except Exception as e:
            raise Exception(e.args[0])
        else:
            return entity_login


