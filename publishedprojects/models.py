from django.db import models
from follow import utils

# Create your models here.
class PublishedProject(models.Model):
	project_link = models.OneToOneField('project.Project', blank=False, null=False, editable = False)
	project_slug_id = models.SlugField(editable = False)

utils.register(PublishedProject)