from django.contrib import admin
from .models import Food , Reasons , Customer , CustomerReasons
# Register your models here.

admin.site.register(Food)
admin.site.register(Reasons)
admin.site.register(CustomerReasons)
