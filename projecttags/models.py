from django.db import models
from project.models import Project
from django.core.validators import RegexValidator

# Create your models here.
class ProjectTag(models.Model):
	alpha = RegexValidator(r'^[a-zA-z\s]*$', 'Can only be alphabetic characters.')
	tag = models.CharField(max_length = 30, validators = [alpha])
	tag_word_index = models.CharField(max_length = 30)
	tag_for_project = models.ManyToManyField(Project, null = True, blank = True)
	def __unicode__(self):
		return unicode("%s" % (self.tag))