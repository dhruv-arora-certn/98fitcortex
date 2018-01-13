from django.db import models

from epilogue.models import Customer
# Create your models here.


class CustomerGoogleClient(models.Model):
	visited = models.DateTimeField(auto_now_add = True)
	customer = models.ForeignKey(Customer , related_name = "gaclientids" , on_delete = models.CASCADE)
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

class EventPageTracking(models.Model):
	url = models.URLField(db_index = True , null = False)
	saved = models.DateTimeField(auto_now_add = True)
	gaclient = models.CharField(max_length = 255)
	referralId = models.CharField(max_length = 255,blank = True)
	event_type = models.CharField(max_length = 100)
	source = models.CharField(max_length = 20 , blank = True)


class UserSignupSource(models.Model):
	customer = models.ForeignKey(Customer, db_index = True , related_name = "signupsource" , on_delete = models.CASCADE)
	source = models.CharField(max_length = 50 , db_index = True)
	campaign = models.CharField(max_length = 50 , null = True)
	language = models.CharField(max_length = 50 , default = "english")
