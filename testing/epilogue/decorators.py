import functools
import datetime

from django.db import models

def last_days(days = 6):
	today = datetime.datetime.today().date()
	while days >= 0:
		val =  today - datetime.timedelta(days = days)
		days -= 1
		yield val

def last_weeks(weeks = 6):
	today = datetime.datetime.today().date()
	current_year , current_week , current_day = today.isocalendar()

	start_week = current_week
	year = current_year

	if start_week >= 6:
		while weeks >= 0:
			yield (year ,current_week)
			current_week -= 1
			weeks -= 1
	else:
		while weeks >= 0:
			yield (year , current_week)
			current_week -= 1
			current_week = abs(52+current_week)%52
			if current_week == 0:
				current_week = 52
				year -= 1
			weeks -= 1

def add_today(f):
	@functools.wraps(f)
	def wrapper(*args , **kwargs):
		kwargs['today'] = datetime.datetime.today().date()
		return f(*args , **kwargs)
	return wrapper

def add_empty_day_in_week(defaults , days_range = 6):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			vals = f(*args , **kwargs)
			days = set(vals.values_list("date" , flat = True))
			data = []
			for e in last_days(days = days_range):
				if e not in days:
					d = {
						"date" : e,
						**defaults,
					}
					data.append(d)
			return data + list(vals)
		return wrapper
	return decorator

def add_empty_weeks(defaults , sort = lambda x : (x['year'],x['week'])):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			weeks , data = f(*args , **kwargs)
			for y,w in last_weeks():
				if (y,w) not in weeks:
					d = {
						"week" : w,
						"year" : y,
						**defaults
					}
					data.append(d)
			return sorted(data , key = sort)
		return wrapper
	return decorator

def sorter(key , reverse = False):
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args , **kwargs):
			vals = f(*args , **kwargs)
			return sorted(vals , key = key , reverse = reverse)
		return wrapper
	return decorator



def scale_field(field,goal):
	def decorator(fn):
		@functools.wraps(fn)
		def wrapper(*args , **kwargs):
			returned_value = fn(*args , **kwargs)
			field_values = (e.get(field) for e in returned_value)
			scaling_factor = 100/(max(goal ,max(field_values)))
			for e in returned_value:
				e['plotting_value'] = e.get(field , 0) * scaling_factor
			return returned_value
		return wrapper
	return decorator

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
					avg = models.Sum(field)
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
