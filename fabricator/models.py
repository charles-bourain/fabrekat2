from django.db import models
from imagestore.models.bases.album import BaseAlbum
from django.contrib.auth.models import User

from account.models import Account
	


#Recommended http://stackoverflow.com/questions/20779068/setting-up-two-different-types-of-users-in-django-1-5-1-6
#Using the regular authentication, and associating the Fabricator to a user via a FK
class Fabricator(models.Model):
	
	fabricator = models.OneToOneField(User, blank=False, null=False, editable = False)
	fabricator_location = models.CharField(max_length=20)
	fabricator_qualifications =  models.CharField(max_length=200)
	fabricator_tools = models.CharField(max_length=20)


	