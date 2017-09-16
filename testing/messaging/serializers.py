from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
	phone = serializers.CharField()

	def validate_phone(self , attrs):
		if not attrs.isdigit():
			raise exceptions.ValidationError("Not a Valid Phone")
		return attrs



