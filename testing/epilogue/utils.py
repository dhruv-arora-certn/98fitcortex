from datetime import datetime
from django.db.models import Max,Sum,Count,Min,Max,Avg
from django.db.models.expressions import RawSQL 
from functools import partial

def get_week(date = datetime.now()):
	return date.isocalendar()[1]

def get_day(date = datetime.now()):
	return date.isocalendar()[2]
	
def get_year(date = datetime.now()):
	return date.isocalendar()[0]

def get_month(date = datetime.now()):
	return date.month

def annotate_avg(qs,field):
	return qs.aggregate(average =  Avg(field))

def annotate_min(qs,field):
	return qs.aggregate( minimum =  Min(field))

def annotate_max(qs,field):
	return qs.aggregate( maximum = Max(field))

def get_monthly_annotation(queryset,field):
	baseQ = queryset.annotate(month = RawSQL("Month(%s)",[field])).annotate(week = RawSQL("FLOOR((DayOfMonth(%s)-1)/7)+1",[field]))
	return baseQ

def get_weekly_annotation(queryset,field):
	baseQ = queryset.annotate(week = RawSQL("Week(%s)",[field])).annotate(day = RawSQL("weekday(%s)+1",[field]))
	return baseQ


class BulkDifferential:

	def getToDelete(self , old , new):
		old_names = [getattr(e , self.BulkMeta.attr_name) for e in old]
		new_names = [getattr(e , self.BulkMeta.attr_name) for e in new]

		common = []
		for e in old:
			if not getattr(e , self.BulkMeta.attr_name) in new_names:
				common.append(e)
		return common

	def getToAdd(self , old , new):
		old_names = [ getattr(e , self.BulkMeta.attr_name) for e in old]
		new_names = [ getattr(e , self.BulkMeta.attr_name) for e in new]

		common = []
		for e in new:
			if not getattr(e , self.BulkMeta.attr_name) in old_names:
				common.append(e)
		return common	
