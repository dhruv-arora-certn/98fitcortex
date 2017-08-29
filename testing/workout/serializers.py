from rest_framework import serializers
from workout.models import WarmupCoolDownMobilityDrillExercise, CardioTimeBasedExercise 


class WarmupCoolDownSerializer(serializers.ModelSerializer):
	class Meta:
		model = WarmupCoolDownMobilityDrillExercise
		fields = "__all__"

class CardioTimeBasedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardioTimeBasedExercise 
		fields = "__all__"
