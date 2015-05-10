from django.db import models
from project.models import Project
from follow import utils

# Create your models here.
class PublishedProject(models.Model):
	project = models.OneToOneField(Project, blank=False, null=False, editable = False)

utils.register(PublishedProject)