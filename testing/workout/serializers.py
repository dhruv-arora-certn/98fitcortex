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
