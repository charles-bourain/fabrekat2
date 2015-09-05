from django.db import models
from django.contrib.auth.models import User
from projectsteps.models import StepOrder, ProjectStep

# Create your models here.


class DesignProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    slug = models.SlugField()
    location = models.CharField(max_length = 30)

    
    def __unicode__(self):  
        return unicode(self.user) 


class WorkingStepOrder(models.Model):
    user = models.ForeignKey(DesignProfile)
    project = models.ForeignKey('publishedprojects.PublishedProject')
    complete = models.BooleanField(default = False)
    steporder = models.ForeignKey(StepOrder, blank = False, null = False)



