from rest_framework import permissions

from .utils import is_valid_week

from django.db.models.expressions import RawSQL
from django.utils.dateparse import parse_datetime

import datetime


class WeekWindowAccessPermission(permissions.BasePermission):
	message = "You cannot access this week's plan"

	def has_permission(self , request , view):
		return True

class IsOwner(permissions.BasePermission):
    '''
    Permission to only access to a user's own data
    '''
    message = "Access Denied"

    def has_object_permission(self, request, view, obj):
        if obj.customer == request.user:
            return True
        return False

class IsLoggingOwn(permissions.BasePermission):
    '''
    Check if the customer id sent is the same as request.user
    '''
    message = "You do not have permission to do this"

    def has_permission(self, request, view):
        if request.data.get("customer"):
            print("Has Customer")
            print(request.data.get("customer"))
            return request.user.id == request.data['customer']
        print("Does not have customer")
        return False


class SingleSleepLog(permissions.BasePermission):
    '''
    Permission to log a single record of sleep
    '''

    def has_permission(self, request, view):
        '''
        Check if the user already has a sleep record for the date of the incoming sleep log
        '''
        border_date = (parse_datetime(request.data['start']) - datetime.timedelta(hours = 5)).date()
        sleep_log = request.user.sleep_logs.annotate(
            date = RawSQL(
                "DATE(DATE_SUB(start, INTERVAL 5 HOUR))",
                []
            )
        )
        sleep_log = sleep_log.filter(
            date = border_date
        )
        if sleep_log.count():
            return False
        return True
