from django.urls import re_path
from .views import SendSMSView

urlpatterns = [
	re_path(r'^send-sms/' , SendSMSView.as_view())
]
