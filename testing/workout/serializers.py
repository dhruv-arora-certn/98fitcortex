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
	name = serializers.CharField()
	description = serializers.CharField()
	duration = serializers.IntegerField()
	duration_unit = serializers.IntegerField()

	def get_name(self ,obj):
		pass

	def get_description(self ,obj):
		pass

	def get_duration(self ,obj):
		pass

	def get_duration_unit(self ,obj):
		pass

class WorkoutSerializer(serializers.Serializer):
	warmup = ExerciseSerialzier(many = True , read_only = True)
	cardio = ExerciseSerialzier(many = True , read_only = True)
	corestrenghtening = ExerciseSerialzier(many = True , read_only = True)
	resistance_training = ExerciseSerialzier(many = True , read_only = True)
	cooldown = ExerciseSerialzier(many = True , read_only = True)
	stretching = ExerciseSerialzier(many = True , read_only = True)
