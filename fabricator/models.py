from django.db import models
from imagestore.models.bases.album import BaseAlbum
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField
from account.models import Account
	


#Recommended http://stackoverflow.com/questions/20779068/setting-up-two-different-types-of-users-in-django-1-5-1-6
#Using the regular authentication, and associating the Fabricator to a user via a FK
class FabricatorType(models.Model):
	fabricator_type = models.CharField(max_length = 20)

	def __unicode__(self):
		return unicode(self.fabricator_type)


class Fabricator(models.Model):
	
	fabricator = models.OneToOneField(User, blank=False, null=False, editable = False)
	fabricator_slug = models.SlugField()
	fabricator_qualifications =  models.CharField(max_length=200)
	fabricator_type = models.ForeignKey(FabricatorType, blank = False, null = False)
	fabricator_blog = models.TextField(max_length = 3000)
	fabricator_location = GeopositionField(default = '47.609490406688096, -122.31884837150574') 

class FabricatorPortfolio(models.Model):
	fabricator = models.OneToOneField(Fabricator)
	fabricator_type_portfolio = models.ForeignKey(FabricatorType, blank = False, null = False)
	portfolio_image = models.ImageField()







#Keeping this seperate so we can add other classes later in site.admin
