from rest_framework import serializers , exceptions
from .models import SMSTracking
from .settings import GSHORTENER_KEY
from .utils import SMS
import requests

class PhoneSerializer(serializers.Serializer):
	phone = serializers.CharField()

	def validate_phone(self , attrs):
		if not attrs.isdigit() or not len(attrs) == 10:
			raise exceptions.ValidationError("Not a Valid Phone")
		return attrs

class SMSSerializer(PhoneSerializer):
	phone = serializers.CharField()
	url = serializers.URLField()
	lang = serializers.CharField()

	def validate_lang(self , lang):
		if lang not in ("en" , "hi"):
			raise exceptions.ValidationError("Not a Valid Language")

	def shorten_url(self , url):
		bUrl = "https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCtjEyqNwpb9mH6TMTroersPmSMsaDT14M"
		r = requests.post(
			bUrl,
			json = {
				'longUrl' :  url
			}
		)
		r.raise_for_status()
		return r.json()['id']

	def get_message(self , s_url):
		return "Thank you for subscribing for the 9 day Navratri Diet Plan on 98Fit.com. Check & follow your plan anytime at: %s"%s_url

	def save(self ):
		url = self.shorten_url(self.validated_data['url'])
		message = self.get_message(url)
		sms = SMS(number = self.validated_data['phone'] , message = message)
		s = SMSTrackingSerializer(data = {
			'phone' : self.validated_data['phone'],
			'message' : self.validated_data['message']
		})
		s.is_valid(raise_exception = True)
		s.save()
		sms.send()

class SMSTrackingSerializer(PhoneSerializer , serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = SMSTracking
	
