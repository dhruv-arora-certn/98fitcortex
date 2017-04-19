from django.contrib import admin
from .models import Food
# Register your models here.
from import_export import resources


class FoodResource(resources.ModelResource):
	class Meta:
		model = Food