from django.db import models
from project.models import Project

# Create your models here.
class ProjectCatagory(models.Model):
	catagory = models.CharField(max_length = 30)
	catagory_word_index = models.CharField(max_length = 30)
	catagory_for_project = models.ManyToManyField(Project, null = True, blank = True)
	def __unicode__(self):
		return unicode("%s" % (self.catagory))