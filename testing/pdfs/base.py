import json

from weasyprint import HTML

from django.template.loader import render_to_string
from . import utils

class PDFBase:

	def __init__(self , *args , **kwargs):
		self.template = kwargs.pop('template')

	def load_file(self):
		filename = self.get_file_name()
		return self.load_data(filename)

	def load_data(self , filename):
		with open(filename) as f:
			data = json.load(f)
		self.data = data
		return self

	def get_file_name(self):
		raise NotImplementedError("This function should be defined")

	def context_data(self):
		return self.data

	def render(self):
		assert hasattr(self , "data") , "load_data() should be called before render"
		context = self.context_data()

		return render_to_string(self.template , context)

	def get_pdf(self):
		self.load_file()
		string = self.render()
		html = HTML(string = string).write_pdf()
		return html

class DiabetesPDF(PDFBase):

	data_template = "disease-data/diabetes-%s-%s-%s.json"
	meals = [
		"m%d"%e for e in range(1,7)
	]

	def __init__(self,*args,**kwargs):

		self.cals = kwargs.pop('cals')
		self.day = kwargs.pop('day')
		self.food_cat = kwargs.pop('food_cat')
		self.user = kwargs.pop('user')

		kwargs['template'] = "guest-diet-diabetes.html"
		super().__init__(*args , **kwargs)

	def get_food_cat(self):
		if self.food_cat in ('veg' , 'egg'):
			return 'veg'
		return 'nonveg'

	def get_file_name(self):
		return self.data_template%(
			self.cals,
			self.day,
			self.get_food_cat()
		)

	def context_data(self):
		context = super().context_data()
		context = list(
			map(
				utils.add_quantity_key , context
			)
		)
		context = utils.mealwise(context , self.meals)
		return {
			**context,
			"user" : self.user,
			"intake" : self.cals
		}

