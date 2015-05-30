from django.db import models

# Create your models here.
class ProjectCatagory(models.Model):
	catagory = models.CharField(max_length = 30)
	def __unicode__(self):
		return unicode("%s" % (self.catagory))