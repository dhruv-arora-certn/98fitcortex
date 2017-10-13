import functools
import datetime


def add_today(f):
	@functools.wraps(f)
	def wrapper(*args , **kwargs):
		kwargs['today'] = datetime.datetime.today().date()
		return f(*args , **kwargs)
	return wrapper
