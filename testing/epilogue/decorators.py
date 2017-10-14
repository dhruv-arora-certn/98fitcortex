import functools
import datetime

from django.db import models 
def add_today(f):
	@functools.wraps(f)
	def wrapper(*args , **kwargs):
		kwargs['today'] = datetime.datetime.today().date()
		return f(*args , **kwargs)
	return wrapper

def weekly_average(field):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			vals = f(*args , **kwargs)
			weeks = set(vals.values_list("week" , flat = True) )
			data = []
			for e in reversed(weeks):
				avg = vals.filter(
					week = e
				).aggregate(
					avg = models.Avg(field)
				)
				d = {
					"week" : e,
					"avg" : avg['avg']
				}
				data.append(d)
			return data
		return wrapper
	return decorator

def monthly_average(field):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(self):
			vals = f(self)
			months = set(vals.values_list("month" , flat = True) )
			data = []
			for e in reversed(months):
				avg = vals.filter(
					month = e
				).aggregate(
					avg = models.Avg(field)
				)
				d = {
					"month" : e,
					"avg" : avg['avg']
				}
				data.append(d)
			return data
		return wrapper
	return decorator

