from django.contrib import admin
from .models import Food , Reasons , Customer , CustomerReasons , CustomerActivityLogs , CustomerWaterLogs , CustomerSleepLogs
# Register your models here.

admin.site.register(Food)
admin.site.register(Reasons)
admin.site.register(CustomerReasons)
admin.site.register(CustomerActivityLogs)
admin.site.register(CustomerWaterLogs)
admin.site.register(CustomerSleepLogs)


#@admin.register(CustomerSleepLogs)
#class SleepAdmin(admin.ModelAdmin):
#    fields = [
#        'customer',
#        'minutes',
#        'start'
#    ]
