from django.db import models


class Product(models.Model):
    name = models.CharField(max_length = 100,blank = True, null = True)
    last_updated = models.DateTimeField(blank = True, null = True)
    price = models.IntegerField(blank = True, null = True)
    ean = models.CharField(max_length = 100,blank = True, null = True, editable = False)
    asin = models.CharField(max_length = 100,blank = True, null = True, editable = False)
    upc = models.CharField(max_length = 100,blank = True, null = True, editable = False)
    currency = models.CharField(max_length = 20,blank = True, null = True)
    url = models.URLField(null = True, blank = True, max_length = 10000)

    def __unicode__(self):
        return unicode(self.name)