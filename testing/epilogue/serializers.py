from rest_framework import serializers , exceptions

from epilogue.models import * 
from epilogue import utils

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django.db.utils import IntegrityError

from passlib.hash import bcrypt

import datetime

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ["id" , "name"]

class CustomerUpdateMixin:
    def update(self, instance, validated_data):
        print("CAlling Customer Update Mixin")
        if 'ls' in validated_data:
            activitylevel_log = instance.activitylevel_logs.create(
                lifestyle = validated_data['ls'],
                year = utils.get_year(),
                week = utils.get_week()
            )
        if 'level' in validated_data:
            level_log = instance.level_logs.create(
                level = validated_data['level'],
                date = datetime.datetime.today(),
                year = utils.get_year(),
                week = utils.get_week()
            )
            print(level_log)
        return super().update(instance, validated_data)

class CustomerSerializer( CustomerUpdateMixin , serializers.ModelSerializer):

    diseases = serializers.StringRelatedField(many = True , source = "customermedicalconditions_set")
    injuries = serializers.StringRelatedField(many = True)
    reasons = serializers.SerializerMethodField()
    height = serializers.CharField(source = "h" , required = False , default = '0.0')
    weight = serializers.CharField(source = "w", required = False , default = '0')
    gender = serializers.CharField(source = "gen", required = False , default = 'female')
    lifestyle = serializers.CharField(source="ls",required = False)
    new_latest_activity = serializers.SerializerMethodField()
    level_in_use = serializers.SerializerMethodField()
    height_type = serializers.IntegerField(source = "h_type", required = False , default= 1)
    weight_type = serializers.IntegerField(source = "w_type", required = False , default = 2)

    class Meta:
        model = Customer
        fields = ["email" , "first_name" , "last_name" , "mobile" , "age" , "weight" , "height", "lifestyle" , "objective" , "id", "gender" , "body_type" , "food_cat" ,"weight_type" , "height_type" , "work_pref" , "level" , "diseases" , "injuries" , "reasons", "new_latest_activity", "current_level", "level_in_use"]

    def get_reasons(self, obj):
        return str(obj.reasons.last())

    def get_lifestyle(self, obj):
        return obj.activity_level_to_use()

    def get_new_latest_activity(self, obj):
        return obj.activity_level_to_use()

    def get_level_in_use(self,obj):
        return obj.fitness_level_to_use()


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["name" , "protein" , "fat" , "carbohydrates" , "image"]

class DietPlanSerializer(serializers.ModelSerializer):
    protein = serializers.SerializerMethodField()
    fat = serializers.SerializerMethodField()
    carbohydrates = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    dietplan_id = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()
    newcalories = serializers.SerializerMethodField()
    preference = serializers.SerializerMethodField()

    class Meta:
        model = GeneratedDietPlanFoodDetails
        fields = "__all__"

    def get_factored_attr(self , attr , obj):
        factor = float(obj.calorie)/float(obj.food_item.calarie)
        return round(getattr(obj.food_item , attr) *factor , 2)

    def get_protein(self , obj):
        return self.get_factored_attr("protein", obj)

    def get_fat(self , obj):
        return self.get_factored_attr("fat", obj)

    def get_carbohydrates(self , obj):
        return self.get_factored_attr("carbohydrates", obj)

    def get_quantity(self , obj):
        if obj.quantity == 0:
            return obj.food_item.quantity
        return obj.quantity

    def get_weight(self , obj):
        if obj.weight == 0:
            return obj.food_item.weight
        return obj.weight

    def get_dietplan_id(self , obj):
        return obj.dietplan.id

    def get_unit(self,  obj):
        if obj.food_item.drink == 1:
            return 'ml'
        return 'gms'

    def get_image(self , obj):
        item = Food.objects.get(pk = obj.food_item_id)
        return item.image
    
    def get_newcalories(self,obj):
        return float(obj.calorie)

    def get_preference(self, obj):
        user = self.context['user']
        pref = user.food_preference.filter(food = obj.food_item).last()

        if pref:
            return pref.preference
        return 0

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(style ={'input_type' : 'password'})

    def validate(self , attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        login_user = None
        login_user = LoginCustomer.objects.filter(email = email)    
        if login_user.count():
            print("login count")
            if self.authenticate(login_user.first() , password):
                attrs['user'] = Customer.objects.filter(email = email).first()
                return attrs
            raise exceptions.ValidationError("Unable to Login with credentials")
        raise exceptions.ValidationError("Unable to login with credentials")

    def authenticate(self , user , password):
        print("inside authenticate")
        return bcrypt.verify(password , user.password)

class CustomerFoodExclusionSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = CustomerFoodExclusions
        fields = "__all__"

class CustomerMedicalConditionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomerMedicalConditions
        fields = "__all__"

class CustomerObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = "__all__"
        
class CreateCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = [ "email" , "first_name" , "last_name" , "mobile" , "age" , "weight" , "height", "lifestyle" , "objective" , "id", "gender" , "body_type" , "food_cat" , "auth_token",  "weight_type" , "height_type", "level" , "current_level"]


    weight = serializers.CharField(source = "w",  required = False)     
    height = serializers.CharField(source = "h",required = False)       
    auth_token = serializers.SerializerMethodField()
    gender = serializers.CharField(source = "gen",required = False)
    lifestyle = serializers.CharField(source = "ls",required = False)
    weight_type = serializers.IntegerField(source = "w_type",required = False)
    height_type = serializers.IntegerField(source = "h_type",required = False)

    def get_auth_token(self , obj):
        return obj.auth_token.key

    def create(self, validated_data):
        instance = super().create(validated_data)


        if 'ls' in validated_data:
            activitylevel_log = instance.activitylevel_logs.create(
                lifestyle = validated_data['ls'],
                year = utils.get_year(),
                week = utils.get_week()
            )
        if 'level' in validated_data:
            level_log = instance.level_logs.create(
                level = validated_data['level'],
                week = utils.get_week(),
                year = utils.get_year()
            )
        return instance

class WaterLoggingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerWaterLogs
        fields = "__all__"

class WaterLoggingSerializer(serializers.Serializer):
    avg  = serializers.FloatField()

class WaterLoggingWeeklySerializer(serializers.Serializer ):
    date =  serializers.DateField()
    day = serializers.SerializerMethodField()
    total_quantity = serializers.FloatField()
    plotting_value = serializers.FloatField()

    def get_day(self , obj):
        print(obj)
        return obj['date'].strftime("%a")

class WaterLoggingMonthlySerializer(serializers.Serializer):
    week = serializers.IntegerField()
    year = serializers.IntegerField()
    sum = serializers.FloatField()
    max = serializers.FloatField()
    min = serializers.FloatField()

class SleepLoggingWeeklySerializer(serializers.Serializer):
    day = serializers.SerializerMethodField()
    date = serializers.DateField()
    total_minutes = serializers.IntegerField()
    plotting_value = serializers.FloatField()
    wakeup = serializers.TimeField(allow_null = True)
    sleep = serializers.TimeField(allow_null = True)

    def get_day(self , obj):
        print(obj)
        return obj['date'].strftime("%a")

class SleepAggregationSerializer(serializers.Serializer):
    minimum = serializers.IntegerField(default = 0 , allow_null = True)
    maximum = serializers.IntegerField(default = 0, allow_null = True)
    average = serializers.FloatField(default = 0, allow_null = True)
    total = serializers.IntegerField(default = 0, allow_null = True)

class WaterAggregationSerializer(SleepAggregationSerializer):
    #while this does not add any functionality , it keeps the namespacing good
    pass

class ActivityAggregationSerializer(SleepAggregationSerializer):
    #while this does not add any functionality , it keeps the namespacing good
    pass

class SleepLoggingMonthlySerializer(serializers.Serializer):
    week = serializers.IntegerField()
    year = serializers.IntegerField()
    avg_minutes = serializers.IntegerField()
    avg_wakeup = serializers.CharField()

class SleepPreviousDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    total_minutes = serializers.IntegerField()

class PlottingSerializer(serializers.Serializer):
    pass

class ActivitySerializer(serializers.Serializer ):
    total_steps = serializers.IntegerField()
    total_cals = serializers.IntegerField()
    total_distance = serializers.IntegerField()
    total_duration = serializers.IntegerField()

class MonthlyActivitySerializer(serializers.Serializer):
    total_steps = serializers.IntegerField()
    total_cals = serializers.IntegerField()
    total_distance = serializers.IntegerField()
    week = serializers.IntegerField()
    year = serializers.IntegerField()

class WeeklyActivitySerializer(ActivitySerializer):
    date = serializers.DateField()
    day = serializers.SerializerMethodField()
    plotting_value = serializers.FloatField()

    def get_day(self , obj):
        return obj['date'].strftime("%a")

class SleepLogginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSleepLogs
        fields = "__all__"

class CustomerActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerActivityLogs
        fields = "__all__"

class CustomerSleepLoggingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSleepLogs
        fields = "__all__"

    def create(self , validated_data):
        start = validated_data['start']
        end = validated_data['end']
        d = end - start
        validated_data['minutes'] = d.total_seconds()//60
        try:
            saved_inst = super().create(validated_data)
        except IntegrityError as int_err :
            #Raised if the record for this day already exists
            raise PermissionDenied("Record for this day already exists")
        else:
            return saved_inst


class CustomerReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReasons
        fields = "__all__"


class CustomerPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFoodItemsPreference
        fields = "__all__"

class WeeklyDietDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedDietPlan
        fields = ["followed","id"]
