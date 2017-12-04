from rest_framework import serializers
from workout.models import WarmupCoolDownMobilityDrillExercise, CardioTimeBasedExercise , NoviceCoreStrengthiningExercise , StretchingExercise , CustomerInjury
import logging

logger = logging.getLogger(__name__)

class WarmupSerializer(serializers.ModelSerializer):
	class Meta:
		model = WarmupCoolDownMobilityDrillExercise
		fields = "__all__"

class CardioTimeBasedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardioTimeBasedExercise
		fields = "__all__"

class NoviceCoreStrengthiningExerciseSerializer(serializers.ModelSerializer):
	class Meta:
		model = NoviceCoreStrengthiningExercise
		fields = "__all__"

class StretchingExerciseSerializer(serializers.ModelSerializer):
	class Meta:
		model = StretchingExercise
		fields = "__all__"

class CoolDownSerializer(serializers.ModelSerializer):
	class Meta:
		model = WarmupCoolDownMobilityDrillExercise
		fields = "__all__"


class ExerciseSerialzier(serializers.Serializer):
	name = serializers.SerializerMethodField()
	description = serializers.SerializerMethodField()
	duration = serializers.SerializerMethodField()
	duration_unit = serializers.SerializerMethodField()
	equipment = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	sets = serializers.SerializerMethodField()
	reps = serializers.SerializerMethodField()
	muscle_group = serializers.SerializerMethodField()
	body_part = serializers.SerializerMethodField()
	exercise_level = serializers.SerializerMethodField()
	exercise_type = serializers.SerializerMethodField()

	def get_name(self ,obj):
		return obj.workout_name

	def get_description(self ,obj):
		description = getattr(obj , "description" , None)
		if description and description.lower().strip() == "na":
			return None
		return description

	def get_duration(self , obj):
		duration =  getattr(obj ,"duration" , None)
		logger.debug("Duration is %s"%duration)
		if duration:
			if int(duration) > 60:
				return int(duration)/60
		return duration

	def get_duration_unit(self , obj):
		duration =  getattr(obj ,"duration" , None)
		if duration:
			if duration > 60:
				return "Minutes"
			else:
				return "Seconds"
		return duration


	def get_equipment(self ,obj):
		equipment = getattr(obj , "machine_name" , None)
		if isinstance(equipment , str) and equipment.lower().strip() == "na":
			return None
		return equipment

	def get_image(self , obj):
		base = "https://s3-ap-southeast-1.amazonaws.com/98fitasset/image/exercise/"
		if hasattr(obj , "image_name") and getattr(obj , "image_name"):
			return "%s%s"%(base,getattr(obj , "image_name" , "http:/www.98fit.com//webroot/workout_images/workout_blank.jpg"))
		return "http://www.98fit.com/webroot/workout_images/workout_blank.jpg"

	def get_sets(self , obj):
		return  getattr(obj , "sets" , None)

	def get_reps(self , obj):
		return  getattr(obj , "reps" , None)

	def get_muscle_group(self , obj):
		return getattr(obj , "muscle_group_name" , None)

	def get_exercise_type(self , obj):
		return getattr(obj , "exercise_type" , None)

	def get_body_part(self , obj):
		return getattr(obj , "body_part" , None)

	def get_exercise_level(self , obj):
		return getattr(obj , "exercise_level" , None)

class WorkoutSerializer(serializers.Serializer):
	warmup = ExerciseSerialzier(many = True , read_only = True)
	cardio = ExerciseSerialzier(many = True , read_only = True)
	corestrenghtening = ExerciseSerialzier(many = True , read_only = True)
	resistance_training = ExerciseSerialzier(many = True , read_only = True)
	cooldown = ExerciseSerialzier(many = True , read_only = True)
	stretching = ExerciseSerialzier(many = True , read_only = True)

class CustomerInjurySerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerInjury
		fields = "__all__"
