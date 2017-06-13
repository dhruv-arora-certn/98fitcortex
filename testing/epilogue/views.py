from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
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
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist
from epilogue.mixins import* 
from django.conf import settings
from rest_framework_bulk import ListBulkCreateAPIView
from django.template.loader import render_to_string
from weasyprint import HTML , CSS
from django.views import View
from datetime import datetime as dt
from .utils import get_day , get_week
import boto3 , datetime
import tempfile

DATE_FORMAT = '%B {S} - %Y, %A'

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
		current_week = get_week(dt.today())

		#If the requested week is farther away than 2 weeks, deny the request
		print("Truth" , abs(abs(week_id) - abs(current_week)))
		if abs(abs(week_id) - abs(current_week)) != 2:
			raise exceptions.PermissionDenied({
				"message" : "You cannot access this week's diet plan"
			})
		
		qs = qs.filter(week_id = int(self.kwargs['week_id'])).last()
		if qs is None:
			p = Pipeline(user.weight , user.height , float(user.lifestyle) , user.goal ,user.gender.number , user = user , persist = True , week = int(week_id))
			try:
				p.generate()
			except Exception as e:
				p.dietplan.delete()
			else: 
				qs = p.dietplan
				g = self.get_diet_plan_details(qs)
				return g

	def get(self , request , *args , **kwargs):
		objs = self.get_object()
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
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = int(self.kwargs.get('day'))).filter(meal_type = self.kwargs.get('meal'))
	
	def get_object(self):
		qs = self.get_queryset().last()
		objs = qs.changeMeal(day = self.kwargs.get('day') , meal = self.kwargs.get('meal'))
		return objs

	def get(self, request , *args , **kwargs):
		objs = self.get_object()
		data = self.serializer_class(objs , many = True).data
		return Response(data)

class CustomerFoodExclusionView(ListBulkCreateAPIView):
	serializer_class = CustomerFoodExclusionSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerFoodExclusions.objects

class CustomerMedicalConditionsView(ListBulkCreateAPIView):
	serializer_class = CustomerMedicalConditionsSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerMedicalConditions.objects

class CreateCustomerView(CreateAPIView):
	serializer_class = CreateCustomerSerializer
	queryset = Customer.objects

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime( t  , format = DATE_FORMAT):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


class GuestPDFView(GenericAPIView):

	def upload_to_s3(self , data):
		import uuid
		session = boto3.Session(
			aws_access_key_id = os.environ.get("S3_ACCESS_KEY"),
			aws_secret_access_key = os.environ.get("S3_ACCESS_SECRET"),
			region_name="ap-south-1"
		)
		s3 = session.resource("s3")
		filename = '/'.join([
			str(uuid.uuid4()),
			"98fit_Diet_Plan_%s.pdf" % (dt.today().strftime("%Y-%m-%d")),
		])
		a = s3.Bucket("98fit-guest-diet-pdfs").put_object(
			Key=filename ,
			Body = data ,
			ACL = "public-read" , 
			Expires = dt.now() + datetime.timedelta(seconds = 60),
		)
		if a:
			return "https://s3.ap-south-1.amazonaws.com/98fit-guest-diet-pdfs/%s"%filename
		return None

	def get_context(self):
		date = custom_strftime(dt.today())
		day = get_day(dt.today())
		user = self.request.user
		dietplan = GeneratedDietPlan.objects.filter( customer = user ).last()
		m1 = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = day).filter(meal_type = 'm1')
		m2 = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = day).filter(meal_type = 'm2')
		m3 = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = day).filter(meal_type = 'm3')
		m4 = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = day).filter(meal_type = 'm4')
		m5 = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = day).filter(meal_type = 'm5')
		return {
			'date' : date,
			'user' : user,
			'm1' : m1,
			'm2' : m2,
			'm3' : m3,
			'm4' : m4,
			'm5' : m5
		}

	def get(self , request):
		self.request = request
		html_string = render_to_string("guest-diet.html" , self.get_context())
		html = HTML(string = html_string)
		result = html.write_pdf()
		url = self.upload_to_s3(result)
		return JsonResponse({
			"url" : url
		})
