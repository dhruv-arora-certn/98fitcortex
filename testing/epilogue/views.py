from django.shortcuts import render
from django.http import HttpResponse
from .forms import AnalysisForm
from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from knapsack.knapsack_dp import knapsack,display
# Create your views here.
import ipdb , random


def get_analysis(request):
	if request.method == "GET":
		form = AnalysisForm()
		return render(request , 'index.html' , {
			'form' : form
		})
	if request.method == "POST":
		form = AnalysisForm(request.POST)
		if form.is_valid():
			form_goal = form.cleaned_data["goals"]
			if form_goal == '0':
				goal = Goals.WeightLoss
			if form_goal == '1':
				goal = Goals.WeightGain
			if form_goal == '2':
				goal = Goals.MaintainWeight
			if form_goal == '3':
				goal = Goals.MuscleGain
			c = Calculations(
				form.cleaned_data['weight'],
				form.cleaned_data['height'],
				float(form.cleaned_data['activity_level']),
				goal,
				exclude = [e for e in form.cleaned_data["exclude"].split(";")]
			)
			# ipdb.set_trace()
			c.makeMeals()
			exclude_c = form.cleaned_data["exclude"].split(";") + c.random
			return render(request , "results.html" , {
				'c' : c,
				'form' : AnalysisForm({
					'exclude' : ";".join(random.sample(exclude_c , min(20 , len(exclude_c)))),
					'weight' : form.cleaned_data['weight'],
					'height' : form.cleaned_data['height'],
					'activity_level' : form.cleaned_data['activity_level'],
					'goals' : form.cleaned_data['goals']
				})
			})
		return HttpResponse('0')
