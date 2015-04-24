import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from filebrowser.base import FileObject
from filebrowser.sites import site
from imagestore.models.bases.album import BaseAlbum
from imagestore.models.bases.image import BaseImage
from follow import utils



#Currently does - /project_image_albums/user_id/project_name/filename.
#I want it to do /project_image_albums/user_id/project_id/filename.
#ISSUE - when this is called, the primary key for project is not created yet, so calling project.id
#	results in none.


class Project(models.Model):

	project_name = models.CharField(max_length=20)
	project_spotlight = models.BooleanField(default=False)
	project_description = models.TextField(max_length= 1000)
	project_creator = models.ForeignKey(User, related_name = 'project_creator_set', editable=False)
	#project_image=models.ImageField(
	#upload_to=get_image_path, 
	#blank=True, 
	#null=True,
	#) 	

	project_time_created = models.DateTimeField(auto_now_add=True, editable=False)
	project_last_modified = models.DateTimeField(auto_now=True, editable=False)
	#project_file = models.FileField(upload_to=get_file_path , blank=True, null=True)

class PurchasedComponent(models.Model):
	purchased_component_for_project = models.ForeignKey(
	Project, 
	blank=True,
	null=True,
	)
	purchased_component_name = models.CharField(max_length = 20)
	purchased_component_url_link = models.URLField()
	purchased_component_quantity = models.IntegerField(default = 0)
	#price = Gotta get the price somehow....

#class FabricatedComponent(models.Model):
#	fabricated_component = models.ForeignKey(Project, 
#		related_name = 'project_fabricated_component',
#		null=True, 
#		blank=True,
#		on_delete=models.SET_NULL,
#	)
#	fabricated_component_quantity = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return unicode(self.project_name)	

class FabricatedComponent(models.Model):
	fabricated_component_for_project = models.ForeignKey(
	Project, 
	blank=True,
	null=True,
	related_name = 'base_project'
	)
	fabricated_component_from_project = models.ForeignKey(
	Project, 
	blank=True,
	related_name = 'component_project'
	)
	fabricated_component_quantity = models.IntegerField(default = 0)
	#price = Gotta get the price somehow....

	def __unicode__(self):
		project_id = fabricated_component_for_project.id

		project_name = models.Project(project_id).project_name


		return unicode(project_name)

#class FabricatedComponent(models.Model):
#	fabricated_component = models.ForeignKey(Project, 
#		related_name = 'project_fabricated_component',
#		null=True, 
#		blank=True,
#		on_delete=models.SET_NULL,
#	)
#	fabricated_component_quantity = models.IntegerField(default = 0)
	
#	def __unicode__(self):
#		return unicode(self.project_name)	


def get_image_path(instance, filename):

		project_id = instance.project_image_for_project_id		
		print project_id
		print filename
		print instance.project_image_for_project

		image_upload_path = os.path.join('project_image_albums',
			'project_%s' % project_id,
			filename
			)

		print image_upload_path

		return image_upload_path	


class ProjectImage(BaseAlbum):
	
	class Meta(BaseAlbum.Meta): 
		app_label = "imagestore" 
		abstract = False		

	project_image_for_project = models.ForeignKey(Project, related_name = 'imageforproject')
	image=models.ImageField(
	upload_to=get_image_path, 
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
		blank=False,
		null=False,
		)
	project_inspired_description = models.TextField(max_length = 400)

class ProjectFile(models.Model):

	def get_file_path(instance, filename):
		project_id = instance.project_file_for_project_id	
		file_upload_path = os.path.join('project_files',
			'project_%s' % project_id,
			filename
			)
		return file_upload_path	

	project_file_for_project = models.ForeignKey(Project)
	file=models.FileField(
	upload_to=get_file_path, 
	blank=True, 
	null=True,
	) 	

		


#Registering Project model with the follows app to allow users to follow Projects
utils.register(Project)