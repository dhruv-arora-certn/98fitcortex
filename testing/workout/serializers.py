from rest_framework import serializers
from workout.models import WarmupCoolDownMobilityDrillExercise, CardioTimeBasedExercise , NoviceCoreStrengthiningExercise , StretchingExercise


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

	def get_name(self ,obj):
		return obj.workout_name

	def get_description(self ,obj):
		pass

	def get_duration(self ,obj):
		return getattr(obj,"duration" , 0)

	def get_duration_unit(self ,obj):
		return "Seconds"

	def get_equipment(self ,obj):
		return "None"

	def get_image(self , obj):
		base = "https://s3-ap-southeast-1.amazonaws.com/98fitasset/image/exercise/"
		if hasattr(obj , "image_name"):
			return "%s%s"%(base,getattr(obj , "image_name" , "http://www.98fit.com//webroot/workout_images/workout_blank.jpg"))
		return "http://www.98fit.com//webroot/workout_images/workout_blank.jpg" 

	def get_sets(self , obj):
		return 0

	def get_reps(self , obj):
		return 0

class WorkoutSerializer(serializers.Serializer):
	warmup = ExerciseSerialzier(many = True , read_only = True)
	cardio = ExerciseSerialzier(many = True , read_only = True)
	corestrenghtening = ExerciseSerialzier(many = True , read_only = True)
	resistance_training = ExerciseSerialzier(many = True , read_only = True)
	cooldown = ExerciseSerialzier(many = True , read_only = True)
	stretching = ExerciseSerialzier(many = True , read_only = True)
