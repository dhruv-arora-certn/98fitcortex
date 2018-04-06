from django.db import models

# Create your models here.

class Devices(models.Model):
    device_id = models.CharField(max_length = 255 , blank = False, null = False)
    registration_id = models.CharField(max_length = 255 )
    customer = models.ForeignKey('epilogue.Customer', on_delete = models.CASCADE)
