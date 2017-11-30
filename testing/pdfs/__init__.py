import json

from weasyprint import HTML
from django.template.loader import render_to_string
from django.utils.timezone import localdate



def add_quantity_key(a):
	if not a.get('quantity'):
		a['quantity'] = 0
	return a
