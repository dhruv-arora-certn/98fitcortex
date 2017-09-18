from django.conf.urls import url
from .views import SendSMSView

urlpatterns = [
	url(r'^send-sms/' , SendSMSView.as_view())
]
