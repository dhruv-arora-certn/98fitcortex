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
from dietplan.generator import Pipeline
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
			p = Pipeline(
				form.cleaned_data['weight'],
				form.cleaned_data['height'],
				float(form.cleaned_data['activity_level']),
				goal,
				float(form.cleaned_data["gender"]),
			)
			# ipdb.set_trace()
			p.generate()
			return render(request , "results.html" , {
				'p' : p,
				'form' : AnalysisForm()
			})
		return HttpResponse('0')
