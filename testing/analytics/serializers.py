from rest_framework import serializers
from . import models


class CustomerGoogleClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerGoogleClient
        fields = "__all__"

class CustomerTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerTracking
        fields = "__all__"

class EventPageTrackingSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.EventPageTracking
            fields = "__all__"

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserFeedback
        fields = "__all__"
