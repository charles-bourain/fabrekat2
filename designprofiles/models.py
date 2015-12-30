from django.db import models
from django.contrib.auth.models import User
from projectsteps.models import StepOrder, ProjectStep
from project.models import Catagory
import os

# Create your models here.


def get_profile_picture_image_path(instance, filename):
    image_upload_path = os.path.join('profile_pictures',
        'user_%s' % instance.user.username
        )

    return image_upload_path


class DesignProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    slug = models.SlugField()
    location = models.CharField(max_length = 30)
    bio = models.CharField(max_length = 5000)
    interest = models.ManyToManyField(Catagory, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=get_profile_picture_image_path, 
        default='default_images/profile_image/no-photo-available-icon.jpg')

    
    def __unicode__(self):  
        return unicode(self.user) 


class WorkingStepOrder(models.Model):
    user = models.ForeignKey(DesignProfile)
    project = models.ForeignKey('publishedprojects.PublishedProject')
    complete = models.BooleanField(default = False)
    steporder = models.ForeignKey(StepOrder, blank = False, null = False)
    in_work = models.BooleanField(default=False)

    def __unicode__(self):  
        return unicode('Project: '+str(self.project.project_link.project_name)+' Is Complete: '+str(self.complete)+' Order #: '+str(self.steporder.order)) 


class DesignerWebsite(models.Model):
    designer = models.ForeignKey(DesignProfile, null=False, blank=False)
    website_url = models.URLField()
