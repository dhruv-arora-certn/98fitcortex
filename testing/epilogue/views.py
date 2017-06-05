from django.shortcuts import render
from django.http import HttpResponse
from .forms import AnalysisForm
from dietplan.goals import Goals
from dietplan.utils import annotate_food
# from dietplan.models import Food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from knapsack.knapsack_dp import knapsack,display
from dietplan.generator import Pipeline
from dietplan.medical_conditions import Osteoporosis , Anemia
from rest_framework.generics import RetrieveUpdateAPIView ,RetrieveAPIView , GenericAPIView , CreateAPIView
from rest_framework.views import APIView
from epilogue.models import *
from epilogue.serializers import *
import ipdb , random
from epilogue.authentication import CustomerAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from epilogue.mixins import *
from django.conf import settings
# from easy_pdf.views import PDFTemplateView


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
			form_disease = form.cleaned_data["disease"]
			print("Form Disease " , form_disease)
			disease = None
			if form_disease == 'Anemia':
				disease = Anemia
			if form_disease == "Osteoporosis":
				disease = Osteoporosis
			print("Final disease is " , disease)	
			p = Pipeline(
				form.cleaned_data['weight'],
				form.cleaned_data['height'],
				float(form.cleaned_data['activity_level']),
				goal,
				float(form.cleaned_data["gender"]),
				disease = disease
			)
			# ipdb.set_trace()
			p.generate()
			return render(request , "results.html" , {
				'p' : p,
				'form' : AnalysisForm()
			})
		return HttpResponse('0')


class UserView(RetrieveUpdateAPIView):
	queryset = Customer.objects
	serializer_class = CustomerSerializer

class DietPlanView(GenericAPIView):
	serializer_class = DietPlanSerializer
	authentication_classes = (CustomerAuthentication,)
	permission_classes = (IsAuthenticated,)
	lookup_fields = ("week_id" , "day")

	def get_queryset(self):
		return GeneratedDietPlan.objects.filter(customer = self.request.user)

	def get_diet_plan_details(self , dietplan ):
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(calorie__gt = 0).filter(day = int(self.kwargs['day'])) 
	
	def get_object(self):
		qs = self.get_queryset()
		user = self.request.user
		week_id = int(self.kwargs.get("week_id"))
		qs = qs.filter(week_id = int(self.kwargs['week_id'])).last()
		if qs is None:
			print("Generating")
			p = Pipeline(user.weight , user.height , float(user.lifestyle) , user.goal ,user.gender.number , user = user , persist = True , week = int(week_id))
			p.generate() 
			qs = p.dietplan
		g = self.get_diet_plan_details(qs)
		return g

	def get(self , request , *args , **kwargs):
		objs = self.get_object()
		# ipdb.set_trace()
		data = DietPlanSerializer(objs , many = True).data
		return Response(data)

class DishReplaceView(RetrieveAPIView):
	serializer_class = DietPlanSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = GeneratedDietPlanFoodDetails.objects

	def get(self , request , *args , **kwargs):
		print("Calling Dish Replace")
		obj = self.get_object()
		a = obj.find_closest(save = True)
		data = self.serializer_class(a).data
		return Response(data)

class MealReplaceView(GenericAPIView):
	serializer_class = DietPlanSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = GeneratedDietPlan.objects

	def get_queryset(self):
		return GeneratedDietPlan.objects.filter(customer = self.request.user).filter(week_id = self.kwargs.get('week_id'))
	
	def get_diet_plan_details(self , dietplan):
		# ipdb.set_trace()
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = int(self.kwargs.get('day'))).filter(meal_type = self.kwargs.get('meal'))
	
	def get_object(self):
		qs = self.get_queryset().last()
		objs = qs.changeMeal(day = self.kwargs.get('day') , meal = self.kwargs.get('meal'))
		return objs

	def get(self, request , *args , **kwargs):
		objs = self.get_object()
		data = self.serializer_class(objs , many = True).data
		return Response(data)

class CustomerFoodExclusionView(CreateAPIView):
	serializer_class = CustomerFoodExclusionSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerFoodExclusions.objects

class CustomerMedicalConditionsView(CreateAPIView):
	serializer_class = CustomerMedicalConditionsSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerMedicalConditions.objects

class CreateCustomerView(CreateAPIView):
	serializer_class = CreateCustomerSerializer
	# authentication_classes = [CustomerAuthentication]
	# permission_classes = [IsAuthenticated]
	queryset = Customer.objects


# class HelloPDF(PDFTemplateView):
# 	template_name = "guest-diet.html"

# 	download_filename = "hello.pdf"

# 	def get_context_data(self,  **kwargs):
# 		return super().get_context_data(
# 			pagesize = 'A4',
# 			title = "Hi",
# 			logo = "http://www.98fit.com/img/Frontend/logo_home.png",
# 			**kwargs
# 		)