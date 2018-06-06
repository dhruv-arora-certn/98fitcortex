import boto3 , datetime , ipdb , random , json
from datetime import datetime as dt

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.db import transaction
from django.core.cache import caches

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
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins

from epilogue.models import *
from epilogue.serializers import *
from epilogue.authentication import CustomerAuthentication
from epilogue.mixins import *
from epilogue.utils import get_day , get_week , BulkDifferential , diabetes_pdf , is_valid_week, check_dietplan_dependencies, get_meals_meta
from epilogue import cache_utils
from epilogue.replacement import *
from epilogue.exceptions import MultipleDiseasesException , DiseasesNotDiabetesOrPcod
from epilogue import permissions as epilogue_permissions
from epilogue import regenerators
from epilogue import disease_utils

from regeneration import views as regeneration_views
from regeneration import signals as regeneration_signals

from workout import utils as workout_utils

from pdfs import base, file_handlers

from weasyprint import HTML

import functools

DATE_FORMAT = '%B {S} - %Y, %A'

class UserGenericAPIView(GenericAPIView):
    '''
    View to assign request.user attributes:
    - level_obj
    - user_relative_workout_week
    '''

    def set_level_obj(self , request):
        '''
        Set level_obj attribute on request.user
        '''
        workout_utils.set_user_level(request, *self.args, **self.kwargs)

    def set_user_relative_workout_week(self, request):
        '''
        Set the user_relative_workout_week attribute on request.user
        '''
        request.user.user_relative_workout_week = workout_utils.get_weeks_since(request, **self.kwargs)

    def initialize_request(self, request, *args, **kwargs):
        '''
        Modify the request.user object to assign
        - level_obj
        - user_relative_workout_week
        '''
        req = super().initialize_request(
            request, *args, **kwargs
        )
        #if the user is not anonymous assign the attributes
        if not req.user.is_anonymous:
            self.set_level_obj(req)
            self.set_user_relative_workout_week(req)

        return req

    def get_week_year_context(self):
        '''
        Get the week and year of the request as a dict
        '''
        kwargs = self.kwargs
        return {
            "week" : int(kwargs.get('week_id')),
            "year" : int(kwargs.get('year'))
        }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not context:
            context = {}
        context['user'] = self.request.user
        return context


class CreateAPICachedView(CreateAPIView):
    '''
    Inherit from this class to invalidate weekly cache

    The inheriting class must have the following attribute:

    - cache_modules = [#modules] //list of cache modules relevant to the class
    '''

    def get_keys(self):
        '''
        Return the keys for cache that are relevant to the view
        '''
        get_key = functools.partial(
            cache_utils.get_cache_key, self.request.user
        )
        keys = [
            get_key(e) for e in self.cache_modules
        ]
        return keys

    def remove_cache_weekly(self):
        '''
        Delete the weekly cache when a data point is added
        '''
        keys = self.get_keys()
        return cache.delete_many(keys)

    def post(self, request, *args, **kwargs):
        self.remove_cache_weekly()
        res = super().post(request, *args, **kwargs)
        return res

class UserView(RetrieveUpdateAPIView):
    queryset = Customer.objects
    serializer_class = CustomerSerializer
    
    def get_serializer_context(self):
        data = super().get_serializer_context()
        data.update({
            'kwargs' : self.kwargs
        })
        return data

class DietPlanView(regeneration_views.RegenerableView):
    serializer_class = DietPlanSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_fields = ("year" , "week_id" , "day")
    queryset = GeneratedDietPlan.objects
    
    def get_regenerate_log_filter(self):
        return {
            'customer' : self.request.user,
            'year' : self.kwargs.get('year'),
            'week' : self.kwargs.get('week_id'),
            'regenerated' : False
        }

    def get_queryset(self):
        return GeneratedDietPlan.objects.filter(customer = self.request.user , year = self.kwargs.get('year') , week_id = self.kwargs.get('week_id'))

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

        file_to_read = "disease-data/diabetes-%s-%s.json"%(cals,self.kwargs['day'])
        print("File" , file_to_read)
        with open(file_to_read , "r") as f:
            return json.load(f) , cals

    def get_object_(self):
        qs = self.get_queryset()
        user = self.request.user
        week_id = int(self.kwargs.get("week_id"))
        year = int(self.kwargs.get("year"))
        current_week = get_week(dt.today())

        #If the requested week is farther away than 2 weeks, deny the request
        print("Truth" , abs(abs(week_id) - abs(current_week)))
        if not is_valid_week(year , week_id):
            raise exceptions.PermissionDenied({
                "message" : "You cannot access this week's diet plan"
            })

        qs = qs.filter(week_id = int(self.kwargs['week_id'])).filter(
            year = int(self.kwargs.get('year'))
        ).last()
        if qs is None:
            p = Pipeline(
                user.latest_weight , 
                user.height , 
                float(user.activity_level_to_use(week = week_id, year = year)) , 
                useractvitiy.goal ,
                user.gender.number , 
                user = user , 
                persist = True , 
                week = week_id , 
                year = year)
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
        print("Diabetes" , request.user.has_diabetes())
        if request.user.has_diabetes():
            data , cals = self.get_diabetes(request.user)
            for e in data:
                if not e.get("image"):
                    e['image'] = "http://98fit.com//webroot/dietlist_images/images.jpg"
            return Response({
                "meta" : {
                    "disease" : "diabetes",
                    "calories" :  cals ,
                    "allow-replace" : False,
                    "user_id": request.user.id,
                    "pdf" : diabetes_pdf(cals , kwargs['day']),
                    "user_week" : request.user.user_week
                },
                "data" : data
            })
        objs = self.get_object()
        return Response(objs)
        data = DietPlanSerializer(objs , many = True).data
        return Response(data)

class DishReplaceView(RetrieveAPIView):
    serializer_class = DietPlanSerializer
    authentication_classes = [CustomerAuthentication]
    permission_classes = [
        IsAuthenticated, epilogue_permissions.IsOwner
    ]
    queryset = GeneratedDietPlanFoodDetails.objects

    def get(self , request , *args , **kwargs):
        print("Calling Dish Replace")
        obj = self.get_object()

        activity_level_to_use = float(self.request.user.activity_level_to_use(
            week = obj.dietplan.week_id,
            year = obj.dietplan.year
        ))
        r = ReplacementPipeline(dish = obj , replaceMeal = False, activity_level_to_use = activity_level_to_use)
        r.meal.build()
        a = r.save()
        if not a:
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )
        data = self.serializer_class(obj, context = {
            "user" : request.user
        }).data
        return Response(data)

class MealReplaceView(UserGenericAPIView):
    serializer_class = DietPlanSerializer
    authentication_classes = [CustomerAuthentication]
    permission_classes = [
        IsAuthenticated, epilogue_permissions.IsOwner
    ]
    queryset = GeneratedDietPlan.objects

    def get_queryset(self):
        return GeneratedDietPlan.objects.filter(customer = self.request.user).filter(year = int(self.kwargs.get('year'))).filter(week_id = self.kwargs.get('week_id'))

    def get_diet_plan_details(self , dietplan):
        return GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = dietplan.id).filter(day = int(self.kwargs.get('day'))).filter(meal_type = self.kwargs.get('meal'))

    def get_object(self):
        qs = self.get_queryset().last()
        objs = self.get_diet_plan_details(qs).last()
        r = ReplacementPipeline(
            dish = objs,
            replaceMeal = True,
            activity_level_to_use = float(self.request.user.activity_level_to_use(
                **self.get_week_year_context()
            ))
        )
        r.meal.build()
        return r.save()

    def get(self, request , *args , **kwargs):
        objs = self.get_object()
        data = self.serializer_class(objs , many = True, context = self.get_serializer_context()).data
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

    def get_queryset(self):
        return self.request.user.customerfoodexclusions_set.all()

    def post(self , request , *args , **kwargs):
        bulk = isinstance(request.data , list)
        if bulk:
            toDelete , toAdd = self.getPartition(request)
            
            if toDelete or toAdd:
                regeneration_signals.diet_regeneration.send(
                    sender = Customer,
                    user = request.user 
                )
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
        new = [CustomerMedicalConditions(customer = request.user , condition_name = e.get('condition_name')) for e in request.data if e.get('condition_name') != "none"]
        return self.getToDelete( old , new ) , self.getToAdd( old , new )

    def get_queryset(self):
        return self.request.user.customermedicalconditions_set.all()

    def post(self, request , *args , **kwargs):
        bulk = isinstance(request.data , list)
        if bulk:
            toDelete , toAdd = self.getPartition(request)

            for e in toDelete:
                e.delete()

            CustomerMedicalConditions.objects.bulk_create(toAdd)
            #for e in toAdd:
            #    e.save()

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
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]

    @classmethod
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

class DiseasePDFView(GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]

    def get_cals(self):
        c = Calculations(*self.request.user.args_attrs)
        rounded_cals = round(c.calories/100)*100
        if rounded_cals <= 1200:
            cals = 1200
        elif rounded_cals == 1300:
            cals = 1300
        else:
            cals = 1400
        return cals

    def get_pdf_attrs(self):
        day = self.kwargs.get('day')
        cals = self.get_cals()
        user = self.request.user
        food_cat = user.food_cat
        return { "day" : day ,
                 "cals" : cals ,
                "user" : user ,
                "food_cat" : food_cat}

    def pcod_pdf(self):
        d = base.PcosPDF(**self.get_pdf_attrs())
        pdf = d.get_pdf()
        url = file_handlers.S3PDFHandler.upload(
            pdf
        )
        return Response({
            "url" : url
        })

    def diabetes_pdf(self):
        d = base.DiabetesPDF(*self.get_pdf_attrs())
        pdf = d.get_pdf()
        url = file_handlers.S3PDFHandler.upload(
            pdf
        )
        return Response({
            "url" : url
        })

    def get(self , request , *args , **kwargs):
        if request.user.has_pcod():
            return self.pcod_pdf()
        elif request.user.has_diabetes():
            return self.diabetes_pdf()

class DietPlanRegenerationView(GenericAPIView):
    serializer_class = DietPlanSerializer
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (IsAuthenticated,) #Add a class to authenticate the owner of the dietplan

    def get_queryset(self):
        return GeneratedDietPlan.objects.get(pk = self.kwargs.get("id"))

    def get_food_cat(self):
        pass

    def get_diabetes(self , user):
        c = Calculations(*user.args_attrs)
        rounded_cals = round(c.calories/100)*100

        if rounded_cals <= 1200:
            cals = 1200
        elif rounded_cals == 1300:
            cals = 1300
        else:
            cals = 1400

        file_to_read = "disease-data/diabetes-%s-%s.json"%(cals,self.kwargs['id'])
        print("File" , file_to_read)
        with open(file_to_read , "r") as f:
            return json.load(f) , cals

    def get_pcos(self,user):
        c = Calculations(*user.args_attrs)
        rounded_cals = round(c.calories/100)*100

        if rounded_cals <= 1200:
            cals = 1200
        elif rounded_cals == 1300:
            cals = 1300
        else:
            cals = 1400

        food_cat = self.request.user.food_cat

        file_to_read = "disease-data/pcos-%s-%s-%s.json"%(cals , self.kwargs['id'] , food_cat)

        print("File" , file_to_read)
        with open(file_to_read , "r") as f:
            return json.load(f) , cals


    def get(self , request , *args , **kwargs):
        print("PCOD" , request.user.has_pcod())
        if request.user.has_diabetes():
            data , cals = self.get_diabetes(request.user)
            for e in data:
                if not e.get("image"):
                    e['image'] = "http://98fit.com//webroot/dietlist_images/images.jpg"
            return Response({
                "meta" : {
                    "disease" : "diabetes",
                    "calories" :  cals ,
                    "allow-replace" : False,
                    "user_id": request.user.id,
                    "pdf" : "http://www.example.com",
                    "user_week" : request.user.user_week if request.user.user_week > 0 else 1
                },
                "data" : data
            })
        if request.user.has_pcod():
            data , cals = self.get_pcos(request.user)
            for e in data:
                if not e.get("image"):
                    e['image'] = "http://98fit.com//webroot/dietlist_images/images.jpg"
            return Response({
                "meta" : {
                    "disease" : "pcod",
                    "calories" :  cals ,
                    "allow-replace" : False,
                    "user_id": request.user.id,
                    "pdf" : "http://www.example.com",
                    "user_week" : request.user.user_week if request.user.user_week > 0 else 1
                },
                "data" : data
            })
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
                    "data"  : {
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
        #   for e in possibleDietPlans:
        #       e.regenerate()
        # except Exception as error:
        #   print("Error is" , error)
        #   return Response({
        #       "message" : str(error)
        #   } , status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
            # return Response({
            #   "weeks" : [e.week_id for e in possibleDietPlans],
            #   "message" : "Successfully Regenrated"
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

        qs = qs.filter(year = int(self.kwargs['year']) , week_id = int(self.kwargs['week_id'])).last()
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

class ActivityLogView(CreateAPICachedView):
    serializer_class = CustomerActivityLogsSerializer
    queryset = CustomerActivityLogs.objects
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    cache_modules = [cache_utils.modules.ACTIVITY_AGGREGATE, cache_utils.modules.ACTIVITY_LOGS]

class SleepWeeklyAggregationView(GenericAPIView):
    authentication_classes = (CustomerAuthentication,)
    permission_classes = (IsAuthenticated ,)

    def serializeWeeklyLogs(self , user,week = None):
        
        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.SLEEP_LOGS)
        if cache.get(key):
            data = cache.get(key)
            print("Cache available")
        else:
            print("Cache not available")
            weekly_logs = user.weekly_sleep(week)[:-1]
            data = SleepLoggingWeeklySerializer(data = list(weekly_logs) , many = True)
            data.is_valid()
            cache.set(key, data, cache_utils.get_time_to_midnight())
        return data.data

    def serializeWeeklyAggregatedLogs(self,user,week = None):

        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.SLEEP_AGGREGATE)
        if cache.get(key):
            data = cache.get(key)
        else:
            aggregated_logs = user.weekly_sleep_aggregated(week)
            data = SleepAggregationSerializer(data = aggregated_logs )
            data.is_valid(raise_exception = True)
            cache.set(key, data, cache_utils.get_time_to_midnight())
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
        aggregated_logs = user.monthly_sleep_aggregate()
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

    def serializeWeeklyLogs(self , user):
        weekly_logs = user.weekly_water()
        data = WaterLoggingWeeklySerializer(
            data = list(weekly_logs),
            many = True
        )
        if data.is_valid():
            return data.data
        return data.errors

    def serializeWeeklyAggregatedLogs(self , user):
        weekly_aggregated_logs = user.weekly_water_aggregate()
        data = WaterAggregationSerializer(data = weekly_aggregated_logs )
        if data.is_valid():
            return data.data
        return data.errors

    def get(self , request , *args , **kwargs):
        user = request.user
        weekly_logs = self.serializeWeeklyLogs(user)
        weekly_aggregated_logs = self.serializeWeeklyAggregatedLogs(user)
        return Response({
            "logs" : weekly_logs,
            "data" : weekly_aggregated_logs
        })

class WaterMonthlyAggregateView(ListAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WaterLoggingMonthlySerializer
    lookup_field = "month"

    def serializeMonthlyLogs(self , user):
        monthly_logs = user.monthly_water()
        data = self.serializer_class(data = list(monthly_logs) , many = True)
        if data.is_valid():
            return data.data
        return data.errors

    def serializerMonthlyAggregatedLogs(self,user):
        monthly_aggregated_logs = user.monthly_water_aggregated()
        data  =  WaterAggregationSerializer(data = monthly_aggregated_logs)
        if data.is_valid():
            return data.data
        return data.errors

    def get(self , request , *args, **kwargs):
        user = request.user
        monthly_logs = self.serializeMonthlyLogs(user)
        monthly_aggregated_logs = self.serializerMonthlyAggregatedLogs(user)

        return Response({
            "data" : monthly_aggregated_logs,
            "logs" : monthly_logs
        })

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

    def serializeWeeklyLogs(self , user):
        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.ACTIVITY_LOGS)
        cached_data = cache.get(key) 
        if cached_data:
            print("Cache Available")
            return cached_data.data
        else:
            logs = user.weekly_activity()
            data = self.serializer_class(data = list(logs) ,many = True)
            if data.is_valid():
                cache.set(key, data, cache_utils.get_time_to_midnight())
            else:
                return data.errors
            return data.data

    def serializerAggregatedLogs(self , user):
        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.ACTIVITY_AGGREGATE)
        cached_data = cache.get(key)
        if cached_data:
            print("Cache is available")
            return cached_data.data
        else:
            aggregated_logs = user.weekly_activity_aggregate()
            data = ActivityAggregationSerializer(data = aggregated_logs)
            if data.is_valid():
                cache.set(key, data, cache_utils.get_time_to_midnight())
            else:
                return data.errors
            return data.data

    def get(self , request , *args , **kwargs):
        user = request.user
        weekly_logs = self.serializeWeeklyLogs(user)
        aggregated_logs = self.serializerAggregatedLogs(user)
        return Response({
            "logs" : weekly_logs,
            "data" : aggregated_logs
        })

class MonthlyActivityView(ListAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MonthlyActivitySerializer
    lookup_field = "month"

    def serializeWeeklyLogs(self , user):
        logs = user.monthly_activity()
        data = self.serializer_class(data = list(logs) ,many = True)
        if data.is_valid():
            return data.data
        return data.errors

    def serializerAggregatedLogs(self , user):
        aggregated_logs = user.monthly_activity_aggregate()
        data = ActivityAggregationSerializer(data = aggregated_logs)
        if data.is_valid():
            return data.data
        return data.errors

    def get(self , request , *args , **kwargs):
        user = request.user
        weekly_logs = self.serializeWeeklyLogs(user)
        aggregated_logs = self.serializerAggregatedLogs(user)
        return Response({
            "logs" : weekly_logs,
            "data" : aggregated_logs
        })

    def get_queryset(self):
        return self.request.user.monthly_activity(month = self.kwargs.get("month"))

class CustomerSleepLoggingView(CreateAPICachedView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated, epilogue_permissions.IsLoggingOwn, epilogue_permissions.SingleSleepLog]
    serializer_class = CustomerSleepLoggingSerializer
    queryset = CustomerSleepLogs.objects
    cache_modules = [cache_utils.modules.SLEEP_AGGREGATE, cache_utils.modules.SLEEP_LOGS]

class DashboardMealTextView(GenericAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]

    def set_cache(self, data):
        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.DIET_DASHBOARD_STRING)
        return cache.set(
            key, data, cache_utils.get_time_to_midnight()
        )
    
    def get_object(self):
        '''
        Return the object

        If cache is available, return from cache, else from get_meal_string_dict
        '''
        key = cache_utils.get_cache_key(self.request.user, cache_utils.modules.DIET_DASHBOARD_STRING)

        cached_data = cache.get(key)
    
        #if cache is available, return
        if cached_data:
            return Response(cached_data)

        #If cache is not available, generate string
        data = self.get_meal_string_dict()
        
        if not data:
            return Response(status = status.HTTP_404_NOT_FOUND)
        return Response(data)

    def get_meal_string_dict(self):
        '''
        Return the meal string dict
        '''
        day = get_day()
        week = get_week()
        year = get_year()

        week_diet_plan = self.request.user.dietplans.filter(week_id = week , year = year).last()

        if not week_diet_plan:
            return None

        today_items = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = week_diet_plan.id , day = day)

        if not today_items:
            return None

        meals = ["m%d"%i for i in range(1,6)]
        string_dict = {
            e : ' + '.join([
                a.food_name for a in today_items.filter(meal_type = e)
            ])
            for e in meals
        }
        self.set_cache(string_dict)
        return string_dict

    def get(self , *args , **kwargs):

        return self.get_object()

class CustomerMedicalConditionsMobileView(GenericAPIView , BulkDifferential):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerMedicalConditionsSerializer

    class BulkMeta:
        attr_name = "condition_name"

    mapper = {
        1 : 'diabetes',
        2 : 'pcod',
        3 : 'thyroid',
        4 : 'osteoporosis',
        5 : 'anaemia',
        6 : 'hyper_Tension',
    }

    def get_partition(self , request):
        old = list(request.user.customermedicalconditions_set.all())
        new = [CustomerMedicalConditions(customer = request.user , condition_name = self.mapper.get(e,e)) for e in request.data]
        return self.getToDelete(old , new) , self.getToAdd(old , new)

    def post(self , request , *args , **kwargs):
        bulk = isinstance(request.data , list)

        if bulk:
            toDelete , toAdd  = self.get_partition(request)

            for e in toDelete:
                e.delete()

            for a in toAdd:
                a.save()
        objs = request.user.customermedicalconditions_set.all()
        serialized = self.serializer_class(objs , many = True)

        return Response(serialized.data,status.HTTP_201_CREATED)

class CustomerFoodExclusionsMobileView(GenericAPIView , BulkDifferential):
    authentication_classes = [CustomerAuthentication]
    serializer_class = CustomerFoodExclusionSerializer

    class BulkMeta:
        attr_name = "food_type"

    mapper = {
        1 : 'nuts',
        2 : 'wheat',
        3 : 'dairy',
        4 : 'egg',
        5 : 'seafood',
        6 : 'lamb',
        7 : 'meat',
        8 : 'beef',
        9 : 'nuts',
        10 : 'poultry',
    }

    def get_partition(self , request):
        old = list(request.user.customerfoodexclusions_set.all())
        new = [CustomerFoodExclusions(customer = request.user , food_type = self.mapper.get(e,e)) for e in request.data if e != 0 ]
        return self.getToDelete(old , new) , self.getToAdd(old , new)

    def post(self , request , *args , **kwargs):
        bulk = isinstance(request.data , list)

        if bulk:
            toDelete , toAdd  = self.get_partition(request)

            for e in toDelete:
                e.delete()

            for a in toAdd:
                a.save()

        objs = request.user.customerfoodexclusions_set.all()
        serialized = self.serializer_class(objs , many = True)
        return Response(serialized.data , status.HTTP_201_CREATED)

class CustomerReasonsView(CreateAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerReasonsSerializer


class RegenerableDietPlanView(UserGenericAPIView, regeneration_views.RegenerableView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [
        IsAuthenticated, epilogue_permissions.IsOwner
    ]
    serializer_class = DietPlanSerializer
    before_hooks = [
        workout_utils.set_user_level,
        workout_utils.check_and_update_activity_level
    ]
    
    def before_request_hook(self, request, *args, **kwargs):
        '''
        Add calls to functions that must be run before the request is responded to
        '''
        [
            f(request, *args, **kwargs) for f in self.before_hooks
        ]
        return 

    def get_object_hook(self):
        week_id, year = self.get_week_year_context().values()
        diet_week = GeneratedDietPlan.objects.filter(
            customer = self.request.user,
            week_id = week_id,
            year = year
        ).last()

        if diet_week:
            return diet_week
        else:
            #No Dietplan is available, so make it
            return self.generate()

    def generate(self):
        user = self.request.user
        p = Pipeline(user.latest_weight , user.height , float(user.activity_level_to_use(**self.get_week_year_context())) , user.goal ,user.gender.number , user = user , persist = True , **self.get_week_year_context())
        try:
            p.generate()
        except Exception as e:
            p.dietplan.delete()
            raise
        else:
            return p.dietplan

    def regeneration_hook(self , obj):
        '''
        Function to call for regenration
        
        Params:
        obj : Dietplan object which has to be regenerated. Instance of 
              epilogue.models.GeneratedDietPlan
        '''
        logger = logging.getLogger("regeneration")
        logger.debug("Regenerating")
        dietplan = obj.regenerate(context = self.get_week_year_context()).dietplan
        self.regen_obj.toggleStatus()
        return dietplan
    
    def satisfied_dependencies(self,request):
        return check_dietplan_dependencies(request.user)
    
    def get_diabetes(self):
        return disease_utils.get_diabetes(self.request.user, int(self.kwargs.get('day',1))) 
    
    def get_pcod(self):
        return disease_utils.get_pcod(self.request.user, int(self.kwargs.get('day',1)))
       

    def get(self , request , *args , **kwargs):

        week,year = self.get_week_year_context().values()
 
        #Check if dependencies are satisfied
        if not self.satisfied_dependencies(request):
            return Response({
                    "message" : "Dependencies not Satisfied"
                },
                status = status.HTTP_424_FAILED_DEPENDENCY
            )

        #Check if the user is allowed to view the plan
        if not is_valid_week(year , week):
            raise exceptions.PermissionDenied({
                "message" : "You cannot access this week's plan"
            })

        #Check and return diabetes plan
        if request.user.has_diabetes():
            return Response(self.get_diabetes())

        #Check and return pcos plan
        if request.user.has_pcod():
            return Response(self.get_pcod())

        #Run the hooks before the request is processed
        self.before_request_hook(request, *args, **kwargs)

        #Get the dietplan object to be served
        obj = self.get_object()

        #Extract the Meals from the dietplan now
        meals = self.get_meals(obj)
        meta = get_meals_meta(meals)
        serialized = self.serializer_class(meals , many = True, context = {
            "request" : request,
            "user" : request.user
        })
        return Response({
            "data" : serialized.data,
            "meta" : meta
        })

    def get_meals(self , obj):
        '''
        Return meals from the dietplan for the requested day
        '''
        assert isinstance(obj , GeneratedDietPlan) , "Instance is Not a GeneratedDietPlan : %s"%type(obj)
        day = self.kwargs.get('day',1)
        meals = GeneratedDietPlanFoodDetails.objects.filter(dietplan__id = obj.id , day = day)
        return meals

    def get_regenerate_log_filter(self):
        return {
            'customer' : self.request.user,
            'regenerated' : False,
            'type' : 'diet',
            **self.get_week_year_context()
        }

class CustomerPreferenceView(CreateAPIView,ListAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerPreferenceSerializer

    def get_queryset(self):
        return self.request.user.food_preference.all()

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        request.data['customer'] = request.user.id
        return request

class CustomerWeeklyDietDetailsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated , epilogue_permissions.IsOwner]
    serializer_class =  WeeklyDietDetailsSerializer
    queryset = GeneratedDietPlan.objects.all()

class DayRegenerationView(UserGenericAPIView):
    authentication_classes = [CustomerAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DietPlanSerializer

    def get_regenerator(self):
        '''
        Regenerate a Day's plan based on the URL parameter passed
        '''
        mapper = {
            "veg" : regenerators.VegRegenerator
        }
        return mapper.get(self.request.GET.get('type'), regenerators.DayRegenator)

    def get(self, request, *args, **kwargs):
        day = int(kwargs.get("day"))
        week = int(kwargs.get("week_id"))
        year = int(kwargs.get("year"))
        regenerator = self.get_regenerator()
        day_ = regenerator(
           request.user,
            day,
            week,
            year
        )
        day_.regenerate()

        objs = GeneratedDietPlanFoodDetails.objects.filter(
            day = day,
            dietplan__id = day_.dietplan.id
        )
        data = self.serializer_class(objs, many = True, context = {
            "request" : request,
            "user" : request.user
        }).data
        meta = get_meals_meta(objs)
        return Response({
            "data" : data,
            "meta" : meta
        })

