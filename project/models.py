import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from filebrowser.base import FileObject
from filebrowser.sites import site
from imagestore.models.bases.album import BaseAlbum
from imagestore.models.bases.image import BaseImage
from django.core.exceptions import ValidationError
from follow import utils
from publishedprojects.models import PublishedProject
from projectpricer.models import Product


#Currently does - /project_image_albums/user_id/project_name/filename.
#I want it to do /project_image_albums/user_id/project_id/filename.
#ISSUE - when this is called, the primary key for project is not created yet, so calling project.id
#   results in none. 


def get_project_image_path(instance, filename):

        project_id = instance.project_image_for_project_id      
        print project_id
        print filename
        print instance.project_image_for_project

        image_upload_path = os.path.join('project_image_albums',
            'project_%s' % project_id,
            filename
            )


        return image_upload_path   

class Project(models.Model):

    project_id = models.SlugField(editable = False)
    project_name = models.CharField(max_length=20)
    project_spotlight = models.BooleanField(default=False)
    project_description = models.TextField(max_length= 1000)
    project_creator = models.ForeignKey(User, related_name = 'project_creator_set', editable=False)
    project_time_created = models.DateTimeField(auto_now_add=True, editable=False)
    project_last_modified = models.DateTimeField(auto_now=True, editable=False)
    inspired_from_project = models.OneToOneField(PublishedProject, null = True, blank = True)
    revised_project = models.OneToOneField('self', null = True, blank = True, editable = False)
    project_id_from_revised_project = models.SlugField(editable = False)

    def __unicode__(self):
        return unicode("%s Created By %s" % (self.project_name, self.project_creator))
    


class ProjectImage(BaseAlbum):
    
    class Meta(BaseAlbum.Meta): 
        app_label = "imagestore" 
        abstract = False        

    project_image_for_project = models.ForeignKey(Project, related_name = 'imageforproject')
    image=models.ImageField(
    upload_to=get_project_image_path, 
    blank=True, 
    null=True,
    )   

    def __unicode__(self):
        return unicode(self.project_image_for_project)


#Inspired From: Should be able to pull ALL information from the Inspired from project.
#Auto-populate a lot of the fields prior to editting.  All creating user to edit things that need to be changed etc.
#Include an area where a descriptions of the deviations occur from the inspired from project.
#SHOULD NOT IMPORT IMAGES.  Optional to import files.
class InspiredProject(models.Model):
    project_inspired_link = models.ForeignKey(
        Project, 
        related_name = 'inspired',
        blank=True,
        null=True,
        )

utils.register(Project)


#Registering Project model with the follows app to allow users to follow Projects
