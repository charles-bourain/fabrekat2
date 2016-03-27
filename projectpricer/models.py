from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 1000,blank = True, null = True)
    last_updated = models.DateTimeField(blank = True, null = True)
    price = models.IntegerField(blank = True, null = True)
    ean = models.CharField(max_length = 1000,blank = True, null = True, editable = False)
    asin = models.CharField(max_length = 1000,blank = True, null = True, editable = False)
    upc = models.CharField(max_length = 1000,blank = True, null = True, editable = False)
    currency = models.CharField(max_length = 20,blank = True, null = True)
    url = models.URLField(max_length = 2000, null = True, blank = True)

    def __unicode__(self):
        return unicode(self.name)