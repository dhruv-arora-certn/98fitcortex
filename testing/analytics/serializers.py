from rest_framework import serializers
from analytics.models import CustomerGoogleClient , CustomerTracking , EventPageTracking , NavratriUserEmailSharing


class CustomerGoogleClientSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerGoogleClient
		fields = "__all__"

class CustomerTrackingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerTracking
		fields = "__all__"

class EventPageTrackingSerializer(serializers.ModelSerializer):
		class Meta:
			model = EventPageTracking
			fields = "__all__"

class NavratriUserEmailSharingSerializer(serializers.ModelSerializer):
	class Meta:
		model = NavratriUserEmailSharing
		fields = "__all__"
	
	def create(self , validated_data):
		return super().create(validated_data)
