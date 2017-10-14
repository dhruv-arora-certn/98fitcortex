from datetime import datetime,timedelta
from django.db import models 
from django.db.models.expressions import RawSQL 
from functools import partial
from weasyprint import HTML
from django.template.loader import render_to_string
import functools
import json

def get_week(date = datetime.now()):
	return date.isocalendar()[1]

def get_day(date = datetime.now()):
	return date.isocalendar()[2]
	
def get_year(date = datetime.now()):
	return date.isocalendar()[0]

def get_month(date = datetime.now()):
	return date.month

def aggregate_avg(field , qs):
	return qs.aggregate(average =  models.Avg(field))

def aggregate_min(field,qs):
	return qs.aggregate( minimum =  models.Min(field))

def aggregate_max(field,qs):
	return qs.aggregate( maximum = models.Max(field))

def aggregate_sum(field,qs):
	return qs.aggregate(total = models.Sum(field))

def previous_day():
	today = datetime.now().date()
	return today - timedelta(days = 1)

def countGlasses(queryset):
		queryset = queryset.annotate(
			glasses =models.Sum(models.Case(
				models.When(
					container__name = "glass",
					then = models.F("count")
				),
				default = 0,
				output_field = models.IntegerField()
			)
		))
		return queryset

def countBottles(queryset):
		queryset = queryset.annotate(
			bottles = models.Sum(models.Case(
				models.When(
					container__name = "bottle",
					then = models.F("count")
				),
				default =0,
				output_field = models.IntegerField()
			))
		)
		return queryset

def diabetes_pdf(cals , day):
	with open("disease-data/pdf-list.json" , "r") as f:
		a = json.load(f)
	return a.get("%s-%s"%(cals,day))

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


