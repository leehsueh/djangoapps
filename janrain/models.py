from django.db import models
from django.contrib.auth.models import User

class JanrainUser(models.Model):
    django_user = models.ForeignKey(User, related_name='django_user')
    provider = models.CharField(max_length=64)
    identifier = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return u'Django username: %s, Provider: %s, Display Name: %s' \
        	% (self.django_user.username, self.provider, self.display_name)

    class Meta:
        ordering = ['django_user', 'provider']