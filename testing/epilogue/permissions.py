from rest_framework import permissions

from .utils import is_valid_week


class WeekWindowAccessPermission(permissions.BasePermission):
	message = "You cannot access this week's plan"

	def has_permission(self , request , view):
		return True

