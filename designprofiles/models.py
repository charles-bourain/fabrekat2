from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DesignProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    location = models.CharField(max_length = 50)
    slug = models.SlugField()
    
    def __unicode__(self):
        return unicode(self.user) 
