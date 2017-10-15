import functools
import datetime

from django.db import models 
def add_today(f):
	@functools.wraps(f)
	def wrapper(*args , **kwargs):
		kwargs['today'] = datetime.datetime.today().date()
		return f(*args , **kwargs)
	return wrapper

def add_empty_day_in_week(defaults):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			vals = f(*args , **kwargs)
			days = set(vals.values_list("date" , flat = True))
			data = []
			pass	
def weekly_average(field):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			vals = f(*args , **kwargs)
			weeks = set(vals.values_list("week" , flat = True) )
			data = []
			curr_week = datetime.datetime.now().isocalendar()[1]
			for e in range(curr_week - 6 , curr_week +1):
				if e not in weeks:
					data.append({
						"week" : e,
						"avg" : 0
					})
					continue
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
			for e in months:
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

def map_transform_queryset(iterable , *fields):
	def decorator(f):
		@functools.wraps(f)
		def mapper(*args , **kwargs):
			l = map(lambda x : functools.partial(x , *fields) , iterable)
			val = f(*args , **kwargs)
			d = {}
			for e in l:
				d.update(**e(val))
			return d
		return mapper
	return decorator
