from rest_framework import serializers
from .settings import GSHORTENER_KEY
from .utils import SMS
import requests

class SMSSerializer(serializers.Serializer):
	phone = serializers.CharField()
	url = serializers.URLField()

	def validate_phone(self , attrs):
		if not attrs.isdigit():
			raise exceptions.ValidationError("Not a Valid Phone")
		return attrs

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
		return "You have been subscribed for daily updates. Access your plan anytime on this link: %s"%s_url

	def save(self ):
		url = self.shorten_url(self.validated_data['url'])
		message = self.get_message(url)
		sms = SMS(number = self.validated_data['phone'] , message = message)
		return sms.send()
