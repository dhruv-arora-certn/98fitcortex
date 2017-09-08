from rest_framework import serializers
from analytics.models import CustomerGoogleClient , CustomerTracking , EventPageTracking


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
