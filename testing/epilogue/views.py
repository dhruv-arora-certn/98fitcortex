import boto3 , datetime , ipdb , random , json
from datetime import datetime as dt

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse , JsonResponse

from dietplan.goals import Goals
from dietplan.utils import annotate_food
from dietplan.calculations import Calculations
from dietplan.bodyTypes import BodyTypes
from dietplan.activity import ActivityLevel
from dietplan.meals import M1 , M5 , M3
from dietplan.generator import Pipeline
from dietplan.medical_conditions import Osteoporosis , Anemia
 
from rest_framework.generics import RetrieveUpdateAPIView ,RetrieveAPIView , GenericAPIView , CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions , status
from rest_framework_bulk import ListBulkCreateAPIView

from epilogue.forms import AnalysisForm
from epilogue.models import *
from epilogue.serializers import *
from epilogue.authentication import CustomerAuthentication
from epilogue.mixins import* 
from epilogue.utils import get_day , get_week , BulkDifferential
from epilogue.replacement import *

from weasyprint import HTML


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
	queryset = GeneratedDietPlan.objects

	def get_queryset(self):
		return GeneratedDietPlan.objects.filter(customer = self.request.user)

	def get_diet_plan_details(self , dietplan ):
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(calorie__gt = 0).filter(day = int(self.kwargs['day']))

	def get_diabetes(self , user):
		c = Calculations(*user.args_attrs)
		rounded_cals = round(c.calories/100)*100
		if rounded_cals <= 1200:
			cals = 1200
		elif rounded_cals == 1300:
			cals = 1300
		else:
			cals = 1400

		file_to_read = "disease-data/diabetes-%s-%s.json"%(1200,self.kwargs['day'])
		with open(file_to_read , "r") as f:
			return json.load(f) , cals

	def get_object(self):
		qs = self.get_queryset()
		user = self.request.user
		week_id = int(self.kwargs.get("week_id"))
		current_week = get_week(dt.today())

		#If the requested week is farther away than 2 weeks, deny the request
		print("Truth" , abs(abs(week_id) - abs(current_week)))
		if abs(abs(week_id) - abs(current_week)) > 2:
			raise exceptions.PermissionDenied({
				"message" : "You cannot access this week's diet plan"
			})

		qs = qs.filter(week_id = int(self.kwargs['week_id'])).last()
		if qs is None:
			p = Pipeline(user.latest_weight , user.height , float(user.latest_activity) , user.goal ,user.gender.number , user = user , persist = True , week = int(week_id))
			try:
				print("Trying to generate")
				p.generate()
			except Exception as e:
				print("There has been a MF exception " , e )
				p.dietplan.delete()
			else:
				qs = p.dietplan
		g = self.get_diet_plan_details(qs)
		return g

	def get(self , request , *args , **kwargs):

		if request.user.has_diabetes():
<<<<<<< HEAD
			data , cals = self.get_diabetes(request.user)
			return Response({
				"meta" : {
					"disease" : "diabetes",
					"calories" :  cals 
				},
				"data" : data
			})
=======
			return Response(self.get_diabetes(request.user))
>>>>>>> 64c2be73e749ef5926c5e1e983f99bcd2dc7f63b

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
		r = ReplacementPipeline(dish = obj , replaceMeal = False)
		r.meal.build()
		a = r.save()
		if not a:
			return Response(
				status = status.HTTP_404_NOT_FOUND
			)
		data = self.serializer_class(obj).data
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
		objs = self.get_diet_plan_details(qs).last()
		r = ReplacementPipeline(dish = objs , replaceMeal = True)
		r.meal.build()
		return r.save()

	def get(self, request , *args , **kwargs):
		objs = self.get_object()
		data = self.serializer_class(objs , many = True).data
		return Response(data)

class CustomerFoodExclusionView(ListBulkCreateAPIView , BulkDifferential):
	serializer_class = CustomerFoodExclusionSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerFoodExclusions.objects

	class BulkMeta:
		attr_name = "food_type"

	def getPartition(self , request):
		old = list(request.user.customerfoodexclusions_set.all())
		new = [CustomerFoodExclusions(customer = request.user , food_type = e.get("food_type")) for e in request.data ]
		return self.getToDelete( old , new) , self.getToAdd( old , new )

	def post(self , request , *args , **kwargs):
		bulk = isinstance(request.data , list)
		if bulk:
			toDelete , toAdd = self.getPartition(request)

			for e in toDelete:
				e.delete()
			for e in toAdd:
				e.save()
		objs = request.user.customerfoodexclusions_set.all()
		data = self.serializer_class(objs , many = True)
		return Response(
			data.data , 
			status = status.HTTP_201_CREATED
		)

class CustomerMedicalConditionsView(ListBulkCreateAPIView , BulkDifferential):
	serializer_class = CustomerMedicalConditionsSerializer
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	queryset = CustomerMedicalConditions.objects

	class BulkMeta:
		attr_name = "condition_name"

	def getPartition(self , request):
		old = list(request.user.customermedicalconditions_set.all())
		new = [CustomerMedicalConditions(customer = request.user , condition_name = e.get('condition_name')) for e in request.data]
		return self.getToDelete( old , new ) , self.getToAdd( old , new )

	def post(self, request , *args , **kwargs):
		bulk = isinstance(request.data , list)
		if bulk:
			toDelete , toAdd = self.getPartition(request)

			for e in toDelete:
				e.delete()

			for e in toAdd:
				e.save()

		objs = request.user.customermedicalconditions_set.all()
		data = self.serializer_class(objs , many = True)
		return Response( data.data , status = status.HTTP_201_CREATED )

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
			ContentType="application/pdf",
			ContentDisposition = "attachment"
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
		arr = [m1 , m2 , m3 , m4 , m5]
		cals = sum(float(item.calorie) for e in arr for item in e)
		protein = sum(float(item.food_item.protein*item.factor) for e in arr for item in e)
		fat = sum(float(item.food_item.fat*item.factor) for e in arr for item in e)
		carbs = sum(float(item.food_item.carbohydrates*item.factor) for e in arr for item in e)
		return {
			'date' : date,
			'user' : user,
			'm1' : m1,
			'm2' : m2,
			'm3' : m3,
			'm4' : m4,
			'm5' : m5,
			'cals' : int(cals),
			'protein' : int(protein),
			'carbs' : int(carbs),
			'fat' : int(fat)
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

class DietPlanRegenerationView(GenericAPIView):
	serializer_class = DietPlanSerializer
	authentication_classes = (CustomerAuthentication,) 
	permission_classes = (IsAuthenticated,) #Add a class to authenticate the owner of the dietplan

	def get_queryset(self):
		return GeneratedDietPlan.objects.get(pk = self.kwargs.get("id"))

	def get(self , request , *args , **kwargs):
		obj = self.get_queryset()
		try:
			obj.regenerate()
		except Exception as e:
			raise exceptions.APIException({
				"message" : "Something Went Wrong",
				"exception" : str(e)
			})
		else:
			return Response(
				status = status.HTTP_200_OK, 
				data = {
					"message" : "Successfully Regenrated Dietplan",
					"data"	: {
						"dietplan" : obj.id
					}
				}
			)

class UserDietPlanRegenerationView(GenericAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self , request , *args , **kwargs):
		user = request.user
		current_week = get_week(dt.today())
		possibleWeeks = [
			current_week,
			current_week + 1,
			current_week + 2
		]
		possibleDietPlans = list(
			GeneratedDietPlan.objects.filter(customer = user).filter(week_id__in = possibleWeeks).all()
		)
		# try:
		# 	for e in possibleDietPlans:
		# 		e.regenerate()
		# except Exception as error:
		# 	print("Error is" , error)
		# 	return Response({
		# 		"message" : str(error)
		# 	} , status = status.HTTP_500_INTERNAL_SERVER_ERROR)
		# else:
			# return Response({
			# 	"weeks" : [e.week_id for e in possibleDietPlans],
			# 	"message" : "Successfully Regenrated"
			# }, status = status.HTTP_200_OK)
		for e in possibleDietPlans:
			e.regenerate()
		return Response({
				"weeks" : [e.week_id for e in possibleDietPlans],
				"message" : "Successfully Regenrated"
			}, status = status.HTTP_200_OK)


class DietPlanMobileView(GenericAPIView):
	serializer_class = DietPlanSerializer
	authentication_classes = (CustomerAuthentication,)
	permission_classes = (IsAuthenticated,)
	lookup_fields = ("week_id" , "day" , "meal")

	def get_queryset(self):
		return GeneratedDietPlan.objects.filter(customer = self.request.user)

	def get_diet_plan_details(self , dietplan ):
		return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(calorie__gt = 0).filter(day = int(self.kwargs['day'])).filter(meal_type = self.kwargs.get("meal"))

	def get_object(self):
		# If user has diabetes	
		if self.request.user.has_diabetes():
			self.get_diabetes()

		qs = self.get_queryset()
		user = self.request.user
		week_id = int(self.kwargs.get("week_id"))
		current_week = get_week(dt.today())

		#If the requested week is farther away than 2 weeks, deny the request
		print("Truth" , abs(abs(week_id) - abs(current_week)))
		if abs(abs(week_id) - abs(current_week)) > 2:
			raise exceptions.PermissionDenied({
				"message" : "You cannot access this week's diet plan"
			})
		
		qs = qs.filter(week_id = int(self.kwargs['week_id'])).last()
		if qs is None:
			p = Pipeline(user.weight , user.height , float(user.lifestyle) , user.goal ,user.gender.number , user = user , persist = True , week = int(week_id))
			try:
				print("Trying to generate")
				p.generate()
			except Exception as e:
				print("There has been a MF exception " , e )
				p.dietplan.delete()
			else:
				qs = p.dietplan
		g = self.get_diet_plan_details(qs)
		return g

	def get(self , request , *args , **kwargs):
		objs = self.get_object()
		data = DietPlanSerializer(objs , many = True).data
		return Response(data)

class WaterBulkView(ListBulkCreateAPIView):
	serializer_class = WaterLoggingModelSerializer
	queryset = CustomerWaterLogs.objects
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]

class ActivityLogView(CreateAPIView):
	serializer_class = CustomerActivityLogsSerializer
	queryset = CustomerActivityLogs.objects
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]

class SleepWeeklyAggregationView(GenericAPIView):
	authentication_classes = (CustomerAuthentication,)
	permission_classes = (IsAuthenticated ,)
	
	def serializeWeeklyLogs(self , user,week = None):
		weekly_logs = user.weekly_sleep(week)
		data = SleepLoggingWeeklySerializer(data = list(weekly_logs) , many = True)
		if data.is_valid():
			return data.data
		return {} 

	def serializeWeeklyAggregatedLogs(self,user,week = None):
		aggregated_logs = user.weekly_sleep_aggregated(week)
		data = SleepAggregationSerializer(data = aggregated_logs )
		if data.is_valid():
			return data.data
		return data.errors 

	def get(self,request , *args ,**kwargs):
		user = request.user
		week = int(kwargs['week'])
		weekly_logs = self.serializeWeeklyLogs(user,week)
		weekly_aggregated_logs = self.serializeWeeklyAggregatedLogs(user,week)
		return Response({
			"logs" : weekly_logs,
			"data" : weekly_aggregated_logs,
			"week" : week
		})

class SleepMonthlyAggregatedView(GenericAPIView):
	authentication_classes = (CustomerAuthentication,)
	permission_classes = (IsAuthenticated,)

	def serializeMonthlyLogs(self,user,month = None):
		monthly_logs = user.monthly_sleep(month)
		print(monthly_logs)
		data = SleepLoggingMonthlySerializer(data = list(monthly_logs) , many = True)		
		return list(monthly_logs)

	def serializeMonthlyAggregatedLogs(self,user,month = None):
		aggregated_logs = user.monthly_sleep_aggregate(month)
		data = SleepAggregationSerializer(data = aggregated_logs)
		if data.is_valid():
			return data.data
		return data.errors
	
	def get(self,request,*args ,**kwargs):
		user = request.user
		month = int(kwargs['month'])
		monthly_logs = self.serializeMonthlyLogs(user , month)
		monthly_aggregated_logs = self.serializeMonthlyAggregatedLogs(user,month)
		return Response({
			"logs" : monthly_logs,
			"data" : monthly_aggregated_logs,
			"month" : month
		})

class WaterWeeklyAggregateView(ListAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = WaterLoggingWeeklySerializer
	lookup_field = "week"	

	def get_queryset(self):
		return self.request.user.weekly_water(week = self.kwargs.get("week"))

class WaterMonthlyAggregateView(ListAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = WaterLoggingMonthlySerializer
	lookup_field = "month"	

	def get_queryset(self):
		return self.request.user.monthly_water(month = self.kwargs.get("month"))

class LastDaySleepView(GenericAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = SleepLogginSerializer
	
	def get_queryset(self):
		return self.request.user.last_day_sleep()
	
	def get(self,request):
		data = self.get_queryset()
		s = self.serializer_class(data)
		return Response(s.data)

class WeeklyActivityView(ListAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = WeeklyActivitySerializer
	lookup_field = "week"

	def get_queryset(self):
		return self.request.user.weekly_activity(week = self.kwargs.get("week"))

class MonthlyActivityView(ListAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = MonthlyActivitySerializer
	lookup_field = "month"
	
	def get_queryset(self):
		return self.request.user.monthly_activity(month = self.kwargs.get("month"))

class CustomerSleepLoggingView(CreateAPIView):
	authentication_classes = [CustomerAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = CustomerSleepLoggingSerializer
	queryset = CustomerSleepLogs.objects
