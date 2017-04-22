from django.contrib import admin
from .models import Food
# Register your models here.
from import_export import resources


admin.site.register(Food)