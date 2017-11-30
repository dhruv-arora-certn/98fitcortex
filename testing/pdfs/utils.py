import json

from weasyprint import HTML
from django.template.loader import render_to_string
from django.utils.timezone import localdate



def add_quantity_key(a):
	if not a.get('quantity'):
		a['quantity'] = 0
	return a

def mealwise(context , meals):
	return {
		e : filter_meal(context , e) for e in meals
	}

def filter_meal(data , meal):
	return list(filter(lambda x : x.get('meal_type') == meal , data))
