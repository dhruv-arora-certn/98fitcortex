from django.db import models

from epilogue.models import Customer
# Create your models here.


class CustomerGoogleClient(models.Model):
	visited = models.DateTimeField(auto_now_add = True)
	customer = models.ForeignKey(Customer , related_name = "gaclientids")
	clientId = models.CharField(max_length = 255)

	class Meta:
		indexes = [
			models.Index(fields = ['customer']),
			models.Index(fields = ['clientId']),
			models.Index(fields = ['customer',  'clientId'])
		]

class CustomerTracking(models.Model):
	url = models.URLField(db_index = True , null = False)
	clientId = models.CharField(max_length = 255)
	visited = models.DateTimeField(auto_now_add = True)
