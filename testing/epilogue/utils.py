from datetime import datetime
from django.db.models import Max,Sum,Count,Min,Max,Avg
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
	return qs.annotate(avg = Avg(field))

def annotate_min(qs,field):
	return qs.annotate(min = Min(field))

def annotate_max(qs,field):
	return qs.annotate(max = Max(field))

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
