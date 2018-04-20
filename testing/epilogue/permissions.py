from rest_framework import permissions

from .utils import is_valid_week


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
