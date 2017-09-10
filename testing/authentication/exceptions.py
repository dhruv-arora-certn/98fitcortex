from rest_framework import exceptions


class UserAlreadyExists(exceptions.ValidationError):
	'''
	Exception to be raised when user with same email already exists
	'''
