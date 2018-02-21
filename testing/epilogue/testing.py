from epilogue.models import Customer
from epilogue.utils import last_days_filter

from django.db.models.expressions import RawSQL 

from django.db.models import When , Case , Value , DateField , CharField

from datetime import time , datetime , timedelta

c = Customer.objects.get(pk = 8)

sleep = last_days_filter(c.sleep_logs.annotate(
    date = RawSQL(
        "Date(start)",[]
    ),
    start_time = RawSQL(
        "Time(start)",[]
    )
))

start_time = time(hour = 0 , minute = 0 , second = 0)
end_time = time(hour= 5 , minute = 0 , second = 0)
when = When(
    start_time__gt = start_time,
    start_time__lt = "05:00:00",
    then = RawSQL(
        "DATE_SUB('start' , interval 30 day)" , []
    ),
)
when2 = When(
    start_time__gt = "05:00:00",
    then = RawSQL(
        "DATE_SUB('start' , interval 0 day)" , []
    ),
)

d = sleep.annotate(
    sleep_date = Case(
        when,
        when2,
        output_field = DateField()
    )
)
