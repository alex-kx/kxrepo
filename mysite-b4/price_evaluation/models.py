from django.db import models

class DevicePrice(models.Model):
	device = models.CharField(max_length=50)
	unit = models.CharField(max_length=20)
	lower_limit = models.FloatField()
	upper_limit = models.FloatField()
	ref_unit_price = models.CharField(max_length=50)
	ref_installation_fee = models.CharField(max_length=50)

# Create your models here.
