from django.db import models


class AmazonPrice(models.Model):
	name = models.CharField(max_length = 20,)
	last_updated = models.DateTimeField()
	price = models.DecimalField(max_digits = 10, decimal_places = 2)
	# is_cheapest = models.BooleanField(default = False)


